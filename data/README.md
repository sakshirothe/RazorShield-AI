# RazorShield Synthetic Dataset Specification

## 1. Overview
This dataset contains **50,000 synthetic e-commerce transactions** generated to benchmark and train the **RazorShield Cost-Sensitive AI Risk Manager** for detecting Return-to-Origin (RTO) and abusive return patterns.

> **DISCLAIMER**: This is a 100% synthetic dataset constructed with fixed random seeds for reproducibility. It does not contain any real customer data, real merchant data, or proprietary Razorpay transaction records.

---

## 2. Target Variable
- **`label`** (binary integer):
  - `0`: Normal transaction (completed successfully, kept by buyer or standard legitimate return).
  - `1`: Risky transaction (resulted in doorstep rejection / RTO, repetitive abusive return, or delivery avoidance).
  - Class Distribution: ~9.5% positive instances (realistic class imbalance for e-commerce return abuse).

---

## 3. Schema & Feature Definitions

| Column | Type | Description |
| :--- | :--- | :--- |
| `transaction_id` | String | Unique transaction identifier (`RZ_100000+`) |
| `customer_id` | String | Customer identity (`CUST_100000+`) |
| `merchant_id` | String | Merchant account identifier (`MERCH_001` - `MERCH_025`) |
| `order_value` | Float | Order value in Indian Rupees (₹200 to ₹35,000+) |
| `payment_method` | String | `COD`, `UPI`, `CREDIT_CARD`, `DEBIT_CARD`, `NET_BANKING` |
| `product_category` | String | `Electronics`, `Fashion & Apparel`, `Beauty & Personal Care`, `Home & Kitchen`, `Footwear`, `Jewelry & Accessories` |
| `quantity` | Integer | Total items in cart (1 to 8) |
| `account_age_days` | Integer | Days elapsed since customer profile creation (1 to 1500) |
| `previous_orders` | Integer | Lifetime completed orders by customer |
| `previous_returns` | Integer | Lifetime returned orders |
| `previous_refunds` | Integer | Lifetime refunded transactions |
| `return_rate` | Float | `previous_returns / max(previous_orders, 1)` |
| `rto_rate` | Float | `previous_rto_count / max(previous_orders, 1)` |
| `days_since_last_order` | Integer | Days since customer's previous checkout |
| `orders_last_7_days` | Integer | Short-term order velocity (burst detection) |
| `orders_last_30_days` | Integer | Monthly order velocity |
| `address_change_count` | Integer | Shipping address modifications on record |
| `device_account_count` | Integer | Number of distinct accounts sharing the same device fingerprint |
| `shipping_distance_km` | Float | Distance between fulfillment hub and recipient delivery address |
| `pincode_risk_score` | Float | Pincode delivery failure risk index (0.0 to 1.0) |
| `delivery_attempts` | Integer | Historical average failed delivery attempts |
| `historical_customer_risk` | Float | Composite customer risk score (0.0 to 1.0) |
| `is_weekend` | Integer | Binary indicator (1 if Saturday/Sunday) |
| `hour_of_day` | Integer | Hour of checkout (0 to 23) |
| `customer_order_frequency`| Float | Lifetime orders per month of account tenure |
| `payment_failure_count` | Integer | Recent payment failures |
| `previous_chargebacks` | Integer | Historical chargeback disputes filed |
| `previous_rto_count` | Integer | Historical orders returned to origin at doorstep |
| `label` | Integer | Ground truth binary outcome (`0` = Clean, `1` = Abusive RTO/Return) |

---

## 4. Modeling Assumptions & Limitations
1. **Behavioral Clusters**: Fraudulent and abusive returns are heavily concentrated in Cash on Delivery (COD) orders with new accounts, shared devices, and high address turnover.
2. **Prepaid Protection**: UPI and Credit Card orders present significantly lower doorstep rejection risk because payment has already cleared prior to dispatch.
3. **Synthetic Constraints**: While statistical distributions model real-world logistics patterns in India, this synthetic data cannot account for evolving real-world adversarial fraud tactics without live retraining.
