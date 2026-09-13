from typing import Dict, Any, List, Tuple
from rag.chunking_and_vectorstore import build_vector_stores, embedding_model


def retrieve_with_score(collection, query_text: str, top_k: int = 3) -> Tuple[List[Dict[str, Any]], float]:
    query_embedding = embedding_model.encode([query_text]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    
    if not results["documents"] or not results["documents"][0]:
        return [], 0.0

    chunks = []
    top_1_sim = 0.0

    for i in range(len(results["documents"][0])):
        dist = results["distances"][0][i]
        sim = 1.0 - dist
        if i == 0:
            top_1_sim = sim
            
        chunks.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "similarity": sim
        })

    return chunks, top_1_sim


def mock_llm_generate(query: str, retrieved_chunks: List[Dict[str, Any]], similarity_threshold: float = 0.38) -> str:
    if not retrieved_chunks or retrieved_chunks[0]["similarity"] < similarity_threshold:
        return "I don't know. The requested information is not available in the Nykaa knowledge base."

    context_str = " ".join([c["text"] for c in retrieved_chunks])
    return f"[MOCK_LLM Grounded Answer]: According to Nykaa policy — {context_str}"


def calibrate_threshold(collection) -> float:
    in_scope_queries = [
        "What is the return window for cosmetics?",
        "How are COD refunds transferred?",
        "What are the delivery SLAs for metro cities?"
    ]
    out_scope_queries = [
        "What is the capital of France?",
        "How do I change a flat car tire?",
        "What is the recipe for chocolate cake?"
    ]

    print("=" * 60)
    print("CALIBRATING SIMILARITY THRESHOLD")
    print("=" * 60)

    in_scope_sims = []
    print("--- In-Scope Queries ---")
    for q in in_scope_queries:
        _, sim = retrieve_with_score(collection, q, top_k=1)
        in_scope_sims.append(sim)
        print(f"Query: '{q}' -> Top-1 Similarity: {sim:.4f}")

    out_scope_sims = []
    print("\n--- Out-of-Scope Queries ---")
    for q in out_scope_queries:
        _, sim = retrieve_with_score(collection, q, top_k=1)
        out_scope_sims.append(sim)
        print(f"Query: '{q}' -> Top-1 Similarity: {sim:.4f}")

    min_in_scope = min(in_scope_sims)
    max_out_scope = max(out_scope_sims)
    
    # Midpoint between minimum in-scope score and maximum out-of-scope score
    chosen_threshold = round((min_in_scope + max_out_scope) / 2, 2)
    
    print("\n--- Empirical Calibration Result ---")
    print(f"Minimum In-Scope Similarity  : {min_in_scope:.4f}")
    print(f"Maximum Out-Scope Similarity : {max_out_scope:.4f}")
    print(f"Calibrated Threshold Selected: {chosen_threshold:.2f}")
    print("=" * 60)

    return chosen_threshold


def run_grounded_generation_demo(collection, threshold: float):
    demo_queries = [
        # 5 In-scope queries
        "What is the return window for beauty products?",
        "Can I exchange an item for a different size?",
        "What happens if payment fails during checkout?",
        "How to claim refund for damaged shipment?",
        "What are the international shipping restrictions for perfumes?",
        # 1 Out-of-scope query
        "Can I book a movie ticket or cinema seat here?"
    ]

    print("\n" + "=" * 60)
    print("GROUNDED GENERATION DEMONSTRATION")
    print("=" * 60)

    for idx, q in enumerate(demo_queries, 1):
        chunks, top_sim = retrieve_with_score(collection, q, top_k=3)
        answer = mock_llm_generate(q, chunks, similarity_threshold=threshold)
        
        print(f"\n[{idx}] User Query: {q}")
        print(f"    Top-1 Similarity Score : {top_sim:.4f}")
        print(f"    Agent Response         : {answer}")


if __name__ == "__main__":
    stores = build_vector_stores()
    coll = stores["sentence_collection"]
    threshold = calibrate_threshold(coll)
    run_grounded_generation_demo(coll, threshold)