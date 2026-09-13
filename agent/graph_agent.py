from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
from agent.tools import extract_order_id, get_order_status
from agent.guardrails import check_input_guardrails
from rag.chunking_and_vectorstore import build_vector_stores
from rag.grounded_generation import retrieve_with_score, mock_llm_generate

STORES = build_vector_stores()
SENTENCE_COLL = STORES["sentence_collection"]

RAG_THRESHOLD = 0.55


class AgentState(TypedDict):
    messages: List[Dict[str, str]]
    user_query: str
    intent: Optional[str]
    order_id: Optional[str]
    response: Optional[str]
    is_safe: bool


def guardrail_node(state: AgentState) -> Dict[str, Any]:
    query = state["user_query"]
    is_safe, message = check_input_guardrails(query)
    if not is_safe:
        return {"is_safe": False, "response": message}
    return {"is_safe": True}


def intent_router_node(state: AgentState) -> Dict[str, Any]:
    if not state.get("is_safe", True):
        return {"intent": "blocked"}

    query = state["user_query"]
    extracted_id = extract_order_id(query)
    
    if extracted_id:
        return {"intent": "order_status", "order_id": extracted_id}

    active_order_id = state.get("order_id")
    if not active_order_id and state.get("messages"):
        for msg in reversed(state["messages"]):
            prev_id = extract_order_id(msg.get("content", ""))
            if prev_id:
                active_order_id = prev_id
                break

    order_keywords = ["order", "package", "item", "delivery", "status", "track", "what was my order"]
    if any(kw in query.lower() for kw in order_keywords) and active_order_id:
        return {"intent": "order_status", "order_id": active_order_id}

    return {"intent": "policy_rag"}


def order_status_node(state: AgentState) -> Dict[str, Any]:
    order_id = state.get("order_id")
    if not order_id:
        return {
            "response": "Please provide a valid Nykaa Order ID (formatted as NYK-XXXXXX, e.g., NYK-100201) so I can retrieve your order status."
        }

    res = get_order_status(order_id)
    if not res["found"]:
        return {"response": res["error"]}

    data = res["data"]
    status = data["status"]

    if status == "DELIVERED":
        msg = f"Order **{data['order_id']}** was delivered on {data['delivery_date']} via {data['carrier']} (Tracking: {data['tracking_number']}). Items: {', '.join(data['items'])}."
    elif status == "IN_TRANSIT":
        msg = f"Order **{data['order_id']}** is currently IN TRANSIT with {data['carrier']} (Tracking: {data['tracking_number']}). Estimated delivery date: {data['estimated_delivery']}."
    elif status == "PROCESSING":
        msg = f"Order **{data['order_id']}** is being processed and prepared for dispatch. Estimated dispatch: {data['estimated_dispatch']}."
    elif status == "CANCELLED":
        msg = f"Order **{data['order_id']}** was CANCELLED. Reason: {data['cancellation_reason']}. Refund Status: {data['refund_status']}."
    else:
        msg = f"Order **{data['order_id']}** status: {status}."

    return {"response": msg}


def policy_rag_node(state: AgentState) -> Dict[str, Any]:
    query = state["user_query"]
    chunks, top_sim = retrieve_with_score(SENTENCE_COLL, query, top_k=3)
    response_text = mock_llm_generate(query, chunks, similarity_threshold=RAG_THRESHOLD)
    return {"response": response_text}


def route_next_node(state: AgentState) -> str:
    intent = state.get("intent")
    if intent == "blocked":
        return END
    elif intent == "order_status":
        return "order_status_node"
    else:
        return "policy_rag_node"


def build_nykaa_agent_graph():
    builder = StateGraph(AgentState)

    builder.add_node("guardrail_node", guardrail_node)
    builder.add_node("intent_router_node", intent_router_node)
    builder.add_node("order_status_node", order_status_node)
    builder.add_node("policy_rag_node", policy_rag_node)

    builder.set_entry_point("guardrail_node")

    builder.add_conditional_edges(
        "guardrail_node",
        lambda state: END if not state.get("is_safe", True) else "intent_router_node"
    )

    builder.add_conditional_edges(
        "intent_router_node",
        route_next_node,
        {
            "order_status_node": "order_status_node",
            "policy_rag_node": "policy_rag_node",
            END: END
        }
    )

    builder.add_edge("order_status_node", END)
    builder.add_edge("policy_rag_node", END)

    return builder.compile()