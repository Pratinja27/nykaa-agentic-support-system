from typing import List, Dict

KB_DOCUMENTS: List[Dict[str, str]] = [
    {
        "doc_id": "KB-001",
        "topic": "Return window by product category",
        "content": (
            "Nykaa provides category-specific return windows to ensure product safety and hygiene. "
            "Unopened beauty and personal care items can be returned within 15 days of delivery. "
            "Apparel, footwear, and home decor items feature a 7-day return policy provided tags remain intact. "
            "Electronics and hair styling tools are returnable within 10 days only if damaged or defective upon arrival."
        )
    },
    {
        "doc_id": "KB-002",
        "topic": "COD refund timelines",
        "content": (
            "Cash on Delivery (COD) refunds are processed directly into the customer's bank account via NEFT transfer. "
            "Upon reverse pickup inspection and approval, the customer receives an SMS link to enter bank account details. "
            "Once details are submitted, the funds are credited within 3 to 5 business days. "
            "Alternatively, customers may opt for instant Nykaa Wallet credit valid for future orders."
        )
    },
    {
        "doc_id": "KB-003",
        "topic": "Delivery SLAs",
        "content": (
            "Standard delivery for metro cities takes 2 to 4 business days from order placement. "
            "Non-metro urban areas and tier-2 locations receive packages within 4 to 7 business days. "
            "Express shipping is available for select pincodes offering guaranteed delivery within 24 to 48 hours. "
            "Remote regions or Jammu & Kashmir and North-Eastern states may take up to 10 business days."
        )
    },
    {
        "doc_id": "KB-004",
        "topic": "Reverse-pickup eligibility",
        "content": (
            "Reverse-pickup services are available free of charge across over 19,000 serviceable pincodes in India. "
            "To qualify, items must be unused, unwashed, and packed in original brand packaging with intact barcodes. "
            "If a pincode is non-serviceable for courier pickup, customers can self-ship the item and claim a shipping reimbursement of up to ₹100. "
            "Hygiene-sensitive items like innerwear, opened lipsticks, and ear-piercing jewelry are non-eligible for reverse pickup."
        )
    },
    {
        "doc_id": "KB-005",
        "topic": "Warranty terms by category",
        "content": (
            "Electronics and beauty appliances carry a standard manufacturer warranty ranging from 1 to 2 years. "
            "Beauty products, cosmetics, and skincare items carry no product warranty beyond guaranteed freshness and shelf life. "
            "Apparel and footwear carry a 30-day manufacturing defect warranty covering zipper or seam failures. "
            "Customers must retain the original tax invoice to claim manufacturer warranty at authorized service centers."
        )
    },
    {
        "doc_id": "KB-006",
        "topic": "Order-cancellation policy",
        "content": (
            "Orders can be cancelled at zero penalty before they are dispatched from the warehouse. "
            "Once an order transitions to Shipped status, direct cancellation via the app is disabled. "
            "Customers can refuse delivery at the doorstep if they no longer wish to receive a dispatched package. "
            "Prepaid cancellations are refunded back to the original payment source within 2 to 4 business days."
        )
    },
    {
        "doc_id": "KB-007",
        "topic": "Loyalty-points redemption policy",
        "content": (
            "Nykaa Reward Points are earned on every completed order across beauty and fashion categories. "
            "Every 100 reward points equal ₹10 in store credit redeemable during final checkout. "
            "Points expire after 12 months from the date of issuance if left unredeemed. "
            "Reward points cannot be redeemed on gift card purchases or applied toward delivery charges."
        )
    },
    {
        "doc_id": "KB-008",
        "topic": "Payment-failure/retry policy",
        "content": (
            "If funds are debited during a failed transaction, banking networks auto-reverse the amount within 48 hours. "
            "Nykaa offers a 15-minute retry window for pending payments directly from the order details screen. "
            "If double debit occurs for a single order ID, the excess amount automatically refunds to the source account within 3 business days. "
            "Payment links created for retry expire after 30 minutes of generation."
        )
    },
    {
        "doc_id": "KB-009",
        "topic": "Size-exchange policy",
        "content": (
            "Apparel and footwear products are eligible for a free one-time size exchange within 7 days of delivery. "
            "Exchanges are subject to inventory availability of the requested alternate size. "
            "The product must be unused with original tags attached and brand packaging undamaged. "
            "If the replacement size is out of stock, a store credit or full refund is initiated automatically upon return."
        )
    },
    {
        "doc_id": "KB-010",
        "topic": "Damaged-item claim process",
        "content": (
            "Claims for damaged, defective, or missing items must be raised within 48 hours of shipment delivery. "
            "Customers must provide clear photos or an unboxing video showing the shipping label and damaged product. "
            "Claims verified by the quality audit team qualify for an immediate free replacement or full refund. "
            "Requests raised after 48 hours of confirmed delivery cannot be processed for damage reimbursement."
        )
    },
    {
        "doc_id": "KB-011",
        "topic": "International shipping restrictions",
        "content": (
            "International shipping is available to select international destinations subject to local customs regulations. "
            "Flammable items, perfumes, nail polishes, and pressurized aerosols are restricted from international air transport. "
            "Customs duties, import taxes, and local clearance fees are responsibility of the customer upon delivery. "
            "International orders are non-returnable and non-exchangeable once shipped from India."
        )
    },
    {
        "doc_id": "KB-012",
        "topic": "Customer-support escalation matrix",
        "content": (
            "Level 1 queries are handled by automated assistant and live chat support available 24/7. "
            "Level 2 escalations are assigned to senior support specialists within 24 hours for unresolved order issues. "
            "Level 3 escalations reach the Nodal Grievance Officer with a resolution guarantee within 3 business days. "
            "High escalation scores automatically priority-route orders directly to Level 2 human specialists."
        )
    }
]


def get_kb_documents() -> List[Dict[str, str]]:
    return KB_DOCUMENTS


if __name__ == "__main__":
    docs = get_kb_documents()
    print(f"Loaded {len(docs)} Knowledge Base documents successfully.")
    for doc in docs:
        print(f"[{doc['doc_id']}] {doc['topic']}")