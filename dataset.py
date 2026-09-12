import random
from collections import Counter
from typing import Dict, List, Any

SEED = 42

CATEGORIES = ["Beauty", "Apparel", "Footwear", "Electronics", "Home"]
CATEGORY_WEIGHTS = [0.45, 0.20, 0.15, 0.10, 0.10]

STATUSES = ["Placed", "Shipped", "Delivered", "Returned", "Refunded"]
STATUS_WEIGHTS = [0.15, 0.25, 0.40, 0.10, 0.10]

PRICE_RANGES = {
    "Beauty": (199, 4999),
    "Apparel": (499, 7999),
    "Footwear": (599, 8999),
    "Electronics": (999, 24999),
    "Home": (399, 5999),
}

PRICE_REASONING = (
    "Price ranges reflect realistic Nykaa e-commerce catalog pricing, "
    "ranging from budget beauty essentials (₹199) to premium beauty electronics (₹24,999)."
)


def generate_dataset(num_orders: int = 45, seed: int = SEED) -> List[Dict[str, Any]]:
    random.seed(seed)
    orders = []

    for i in range(1, num_orders + 1):
        record_id = f"NYK-{i:04d}"
        category = random.choices(CATEGORIES, weights=CATEGORY_WEIGHTS, k=1)[0]
        status = random.choices(STATUSES, weights=STATUS_WEIGHTS, k=1)[0]
        
        min_p, max_p = PRICE_RANGES[category]
        order_value_inr = random.randint(min_p, max_p)
        days_since_created = random.randint(0, 30)
        
        if status in ["Placed", "Shipped"] and days_since_created > 5:
            delayed_shipment = random.random() < 0.60
        else:
            delayed_shipment = random.random() < 0.12
        
        orders.append({
            "record_id": record_id,
            "category": category,
            "status": status,
            "order_value_inr": order_value_inr,
            "days_since_created": days_since_created,
            "delayed_shipment": delayed_shipment,
        })

    cat_counts = Counter(o["category"] for o in orders)
    status_counts = Counter(o["status"] for o in orders)
    total_delayed = sum(1 for o in orders if o["delayed_shipment"])
    delay_percentage = (total_delayed / num_orders) * 100

    for cat in CATEGORIES:
        if cat_counts[cat] < 3:
            raise ValueError(f"Category '{cat}' has fewer than 3 records ({cat_counts[cat]}).")

    for st in STATUSES:
        if status_counts[st] < 1:
            raise ValueError(f"Status '{st}' does not appear in dataset.")

    if not (10.0 <= delay_percentage <= 30.0):
        raise ValueError(f"Delayed shipment percentage is {delay_percentage:.2f}%, outside 10%-30%.")

    return orders


ORDERS = generate_dataset()


def print_dataset_report(orders_list: List[Dict[str, Any]]) -> None:
    total_orders = len(orders_list)
    cat_counts = Counter(o["category"] for o in orders_list)
    status_counts = Counter(o["status"] for o in orders_list)
    total_delayed = sum(1 for o in orders_list if o["delayed_shipment"])
    delay_percentage = (total_delayed / total_orders) * 100

    print("=" * 60)
    print("NYKAA SUPPORT AGENT — DATASET REPORT")
    print("=" * 60)
    print(f"Total Records Generated : {total_orders}")
    print(f"Random Seed Used        : {SEED}\n")
    
    print("--- Category Distribution ---")
    for cat, count in cat_counts.items():
        print(f"  - {cat:<12}: {count} records ({count/total_orders*100:.1f}%)")
        
    print("\n--- Status Distribution ---")
    for st, count in status_counts.items():
        print(f"  - {st:<12}: {count} records ({count/total_orders*100:.1f}%)")
        
    print("\n--- Shipment Delay Report ---")
    print(f"  - Delayed Orders      : {total_delayed} / {total_orders}")
    print(f"  - Delay Percentage    : {delay_percentage:.2f}%")
    
    print("\n--- Price Range Reasoning ---")
    print(f"  - {PRICE_REASONING}")
    print("=" * 60)


if __name__ == "__main__":
    print_dataset_report(ORDERS)