import os
import argparse
import numpy as np
import pandas as pd

def generate_dataset(n_samples: int = 50000, seed: int = 42, output_path: str = "data/transactions.csv") -> pd.DataFrame:
    np.random.seed(seed)

    n_unique_customers = int(n_samples * 0.4)
    customer_ids = [f"CUST_{100000 + i}" for i in range(n_unique_customers)]
    customer_pool = np.random.choice(customer_ids, size=n_samples)

    merchants = [f"MERCH_{i:03d}" for i in range(1, 26)]
    merchant_pool = np.random.choice(merchants, size=n_samples)

    product_categories = [
        "Electronics", "Fashion & Apparel", "Beauty & Personal Care",
        "Home & Kitchen", "Footwear", "Jewelry & Accessories"
    ]
    product_category_weights = [0.25, 0.30, 0.15, 0.15, 0.10, 0.05]
    categories = np.random.choice(product_categories, size=n_samples, p=product_category_weights)

    payment_methods = ["COD", "UPI", "CREDIT_CARD", "DEBIT_CARD", "NET_BANKING"]
    payment_weights = [0.35, 0.40, 0.15, 0.07, 0.03]
    payments = np.random.choice(payment_methods, size=n_samples, p=payment_weights)

    quantities = np.random.choice([1, 2, 3, 4, 5, 8], size=n_samples, p=[0.60, 0.22, 0.10, 0.05, 0.02, 0.01])
    base_category_prices = {
        "Electronics": (1500, 32000),
        "Fashion & Apparel": (499, 4500),
        "Beauty & Personal Care": (299, 2500),
        "Home & Kitchen": (699, 8500),
        "Footwear": (799, 6500),
        "Jewelry & Accessories": (1200, 18000)
    }

    order_values = []
    for cat, qty in zip(categories, quantities):
        low, high = base_category_prices[cat]
        unit_val = np.random.exponential(scale=(high - low) / 3) + low
        unit_val = min(unit_val, high * 1.2)
        order_values.append(round(unit_val * qty, 2))
    order_values = np.array(order_values)

    account_age_days = np.random.exponential(scale=200, size=n_samples).astype(int)
    account_age_days = np.clip(account_age_days, 1, 1500)

    expected_orders = np.clip((account_age_days / 30) * np.random.uniform(0.2, 2.5, size=n_samples), 0, 80).astype(int)
    previous_orders = expected_orders

    is_latent_abuser = np.random.binomial(1, 0.08, size=n_samples)
    
    latent_return_tendency = np.where(
        is_latent_abuser == 1,
        np.random.beta(4, 5, size=n_samples),
        np.random.beta(1, 20, size=n_samples)
    )

    previous_returns = np.round(previous_orders * latent_return_tendency).astype(int)
    previous_returns = np.minimum(previous_returns, previous_orders)

    latent_rto_tendency = np.where(
        is_latent_abuser == 1,
        np.random.beta(3, 4, size=n_samples) * 0.7,
        np.random.beta(1, 30, size=n_samples) * 0.3
    )
    previous_rto_count = np.round(previous_orders * latent_rto_tendency).astype(int)
    previous_rto_count = np.minimum(previous_rto_count, previous_orders)

    previous_refunds = np.clip(previous_returns + np.random.choice([0, 1], size=n_samples, p=[0.85, 0.15]), 0, previous_orders)
    previous_chargebacks = np.where(is_latent_abuser == 1, np.random.choice([0, 1, 2], size=n_samples, p=[0.7, 0.2, 0.1]), 0)

    return_rate = np.zeros(n_samples, dtype=float)
    np.divide(previous_returns, previous_orders, out=return_rate, where=(previous_orders > 0))
    return_rate = np.round(return_rate, 4)

    rto_rate = np.zeros(n_samples, dtype=float)
    np.divide(previous_rto_count, previous_orders, out=rto_rate, where=(previous_orders > 0))
    rto_rate = np.round(rto_rate, 4)

    days_since_last_order = np.clip(np.random.exponential(scale=25, size=n_samples).astype(int), 1, 365)
    orders_last_7_days = np.clip(np.random.poisson(lam=0.4 + (is_latent_abuser * 1.5), size=n_samples), 0, 15)
    orders_last_30_days = np.clip(orders_last_7_days + np.random.poisson(lam=1.5, size=n_samples), 0, 35)

    customer_order_frequency = np.round(previous_orders / np.maximum(account_age_days / 30, 1.0), 2)

    device_account_count = np.where(
        is_latent_abuser == 1,
        np.random.choice([1, 2, 3, 4, 5, 6], size=n_samples, p=[0.2, 0.3, 0.25, 0.15, 0.07, 0.03]),
        np.random.choice([1, 2, 3], size=n_samples, p=[0.88, 0.10, 0.02])
    )

    address_change_count = np.where(
        is_latent_abuser == 1,
        np.random.choice([0, 1, 2, 3, 4], size=n_samples, p=[0.25, 0.35, 0.25, 0.10, 0.05]),
        np.random.choice([0, 1, 2], size=n_samples, p=[0.75, 0.20, 0.05])
    )

    shipping_distance_km = np.round(np.random.gamma(shape=3.0, scale=250.0, size=n_samples), 1)
    shipping_distance_km = np.clip(shipping_distance_km, 5.0, 2800.0)

    pincode_risk_score = np.random.beta(a=2.0, b=5.0, size=n_samples)
    pincode_risk_score = np.round(pincode_risk_score, 4)

    delivery_attempts = np.random.choice([0, 1, 2, 3], size=n_samples, p=[0.65, 0.25, 0.08, 0.02])
    payment_failure_count = np.clip(np.random.poisson(lam=0.3 + (is_latent_abuser * 1.2), size=n_samples), 0, 10)

    hour_of_day = np.random.randint(0, 24, size=n_samples)
    is_weekend = np.random.choice([0, 1], size=n_samples, p=[0.71, 0.29])

    historical_customer_risk = np.round(
        np.clip(
            (0.35 * return_rate) +
            (0.35 * rto_rate) +
            (0.15 * (device_account_count - 1) / 5.0) +
            (0.15 * np.minimum(payment_failure_count, 5) / 5.0),
            0.0, 1.0
        ), 4
    )

    cod_flag = (payments == "COD").astype(float)
    fresh_account_flag = (account_age_days < 20).astype(float)
    high_val_flag = (order_values > 4000).astype(float)

    logit = (
        -3.6
        + 1.85 * cod_flag
        + 2.20 * (rto_rate > 0.25).astype(float)
        + 1.70 * (return_rate > 0.30).astype(float)
        + 1.40 * (device_account_count >= 3).astype(float)
        + 1.10 * (address_change_count >= 2).astype(float)
        + 1.35 * (fresh_account_flag * cod_flag * high_val_flag)
        + 1.20 * (pincode_risk_score > 0.65).astype(float)
        + 0.85 * (orders_last_7_days >= 4).astype(float)
        + 0.75 * (payment_failure_count >= 2).astype(float)
        + 0.50 * (shipping_distance_km > 1500).astype(float)
        - 1.10 * (payments == "UPI").astype(float)
        - 1.30 * (payments == "CREDIT_CARD").astype(float)
        - 0.90 * (account_age_days > 180).astype(float) * (return_rate < 0.08).astype(float)
    )

    risk_prob = 1.0 / (1.0 + np.exp(-logit))
    labels = (np.random.uniform(0, 1, size=n_samples) < risk_prob).astype(int)

    txn_ids = [f"RZ_{100000 + i}" for i in range(n_samples)]

    df = pd.DataFrame({
        "transaction_id": txn_ids,
        "customer_id": customer_pool,
        "merchant_id": merchant_pool,
        "order_value": order_values,
        "payment_method": payments,
        "product_category": categories,
        "quantity": quantities,
        "account_age_days": account_age_days,
        "previous_orders": previous_orders,
        "previous_returns": previous_returns,
        "previous_refunds": previous_refunds,
        "return_rate": return_rate,
        "rto_rate": rto_rate,
        "days_since_last_order": days_since_last_order,
        "orders_last_7_days": orders_last_7_days,
        "orders_last_30_days": orders_last_30_days,
        "address_change_count": address_change_count,
        "device_account_count": device_account_count,
        "shipping_distance_km": shipping_distance_km,
        "pincode_risk_score": pincode_risk_score,
        "delivery_attempts": delivery_attempts,
        "historical_customer_risk": historical_customer_risk,
        "is_weekend": is_weekend,
        "hour_of_day": hour_of_day,
        "customer_order_frequency": customer_order_frequency,
        "payment_failure_count": payment_failure_count,
        "previous_chargebacks": previous_chargebacks,
        "previous_rto_count": previous_rto_count,
        "label": labels
    })

    abs_out = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(abs_out), exist_ok=True)
    df.to_csv(abs_out, index=False)
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=50000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=str, default="data/transactions.csv")
    args = parser.parse_args()

    generate_dataset(n_samples=args.samples, seed=args.seed, output_path=args.output)
