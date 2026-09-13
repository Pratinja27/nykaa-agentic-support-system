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

### Knowledge Base Documents
Contains 12 policy documents covering mandatory e-commerce topics:
1. Return window by product category
2. COD refund timelines
3. Delivery SLAs
4. Reverse-pickup eligibility
5. Warranty terms by category
6. Order-cancellation policy
7. Loyalty-points redemption policy
8. Payment-failure/retry policy
9. Size-exchange policy
10. Damaged-item claim process
11. International shipping restrictions
12. Customer-support escalation matrix

### Similarity Threshold Calibration & Grounded Generation
- **Measured In-Scope Cluster Top-1 Similarity:** ~0.55 – 0.85
- **Measured Out-of-Scope Cluster Top-1 Similarity:** ~0.10 – 0.25
- **Empirically Calibrated Threshold:** `0.40`
- **Fallback Behavior:** Out-of-scope queries below `0.40` trigger exact fallback: `"I don't know. The requested information is not available in the Nykaa knowledge base."`

### RAG Strategy Evaluation & Comparison (Precision@3 / Recall@3)
- **Fixed-Size Chunking:** Deduplicates parent documents across fixed slices; average Precision@3 and Recall@3 calculated per query.
- **Sentence-Based Chunking:** Evaluated on natural boundaries.
- **Recommendation:** Sentence-based chunking is selected for agent integration. Sentence-level boundaries preserve complete semantic context without sentence truncation, resulting in higher retrieval precision.