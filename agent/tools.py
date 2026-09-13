import re
from typing import Dict, Any, Optional

# Mock Order Database
MOCK_ORDER_DB: Dict[str, Dict[str, Any]] = {
    "NYK-100201": {
        "order_id": "NYK-100201",
        "status": "DELIVERED",
        "items": ["Maybelline Matte Lipstick", "Cetaphil Cleanser"],
        "delivery_date": "2024-03-01",
        "tracking_number": "TRK98765432",
        "carrier": "BlueDart"
    },
    "NYK-100202": {
        "order_id": "NYK-100202",
        "status": "IN_TRANSIT",
        "items": ["L'Oreal Paris Hair Serum"],
        "estimated_delivery": "2024-03-08",
        "tracking_number": "TRK12345678",
        "carrier": "Delhivery"
    },
    "NYK-100203": {
        "order_id": "NYK-100203",
        "status": "PROCESSING",
        "items": ["Nykaa Beauty Blender", "Kama Ayurveda Face Scrub"],
        "estimated_dispatch": "2024-03-06",
        "tracking_number": None,
        "carrier": "Pending"
    },
    "NYK-100204": {
        "order_id": "NYK-100204",
        "status": "CANCELLED",
        "items": ["Minimalist Salicylic Acid Serum"],
        "cancellation_reason": "Requested by customer during processing",
        "refund_status": "COMPLETED_TO_ORIGINAL_SOURCE"
    }
}


def extract_order_id(text: str) -> Optional[str]:
    """Extracts Order ID matching pattern NYK-XXXXXX (case-insensitive)."""
    match = re.search(r"NYK-\d{6}", text, re.IGNORECASE)
    return match.group(0).upper() if match else None


def get_order_status(order_id: str) -> Dict[str, Any]:
    """Deterministic tool to query order database by Order ID."""
    clean_id = order_id.strip().upper()
    if clean_id in MOCK_ORDER_DB:
        return {
            "found": True,
            "data": MOCK_ORDER_DB[clean_id]
        }
    return {
        "found": False,
        "error": f"Order ID '{clean_id}' was not found in the Nykaa tracking system. Please check your order reference number."
    }