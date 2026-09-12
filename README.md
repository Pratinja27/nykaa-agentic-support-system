# Nykaa Support Agent — Capstone Project

**Track:** E-commerce & Retail  
**Brand:** Nykaa  

## Part 1 — Dataset Design & RAG Core

### Dataset Specifications
- **Seed:** `42`
- **Total Records:** 45 orders (Deterministic generation)
- **Category Weights:** Beauty (45%), Apparel (20%), Footwear (15%), Electronics (10%), Home (10%)
- **Status Weights:** Delivered (40%), Shipped (25%), Placed (15%), Returned (10%), Refunded (10%)
- **Amount Ranges (INR):**
  - Beauty: ₹199 – ₹4,999
  - Apparel: ₹499 – ₹7,999
  - Footwear: ₹599 – ₹8,999
  - Electronics: ₹999 – ₹24,999
  - Home: ₹399 – ₹5,999
- **Price Range Reasoning:** Price ranges reflect realistic Nykaa e-commerce catalog pricing, ranging from budget beauty essentials (₹199) to premium beauty electronics (₹24,999).
- **Delayed Shipment Target:** 10% – 30% (Validated dynamically by generator).