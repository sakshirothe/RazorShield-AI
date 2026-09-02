from typing import Dict, List, Any, Union
import numpy as np
import pandas as pd

PAYMENT_METHODS = ["COD", "UPI", "CREDIT_CARD", "DEBIT_CARD", "NET_BANKING"]
PRODUCT_CATEGORIES = [
    "Electronics", "Fashion & Apparel", "Beauty & Personal Care",
    "Home & Kitchen", "Footwear", "Jewelry & Accessories"
]

FEATURE_COLUMNS = [
    "order_value",
    "quantity",
    "account_age_days",
    "previous_orders",
    "previous_returns",
    "previous_refunds",
    "return_rate",
    "rto_rate",
    "refund_rate",
    "orders_per_week",
    "orders_last_30_days",
    "account_activity_score",
    "device_reuse_score",
    "address_change_frequency",
    "high_value_order_flag",
    "high_value_cod_flag",
    "customer_history_score",
    "pincode_risk",
    "payment_reliability_score",
    "shipping_distance_km",
    "delivery_attempts",
    "is_weekend",
    "hour_of_day",
    "days_since_last_order",
    "pay_COD",
    "pay_UPI",
    "pay_CREDIT_CARD",
    "pay_DEBIT_CARD",
    "pay_NET_BANKING",
    "cat_Electronics",
    "cat_Fashion_Apparel",
    "cat_Beauty_Personal_Care",
    "cat_Home_Kitchen",
    "cat_Footwear",
    "cat_Jewelry_Accessories"
]

def engineer_features(data: Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]]) -> pd.DataFrame:
    if isinstance(data, dict):
        df = pd.DataFrame([data])
    elif isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = data.copy()

    n = len(df)

    order_value = df.get("order_value", pd.Series(np.zeros(n))).astype(float).fillna(1000.0)
    quantity = df.get("quantity", pd.Series(np.ones(n))).astype(float).fillna(1.0)
    account_age_days = df.get("account_age_days", pd.Series(np.zeros(n))).astype(float).fillna(30.0)
    previous_orders = df.get("previous_orders", pd.Series(np.zeros(n))).astype(float).fillna(0.0)
    previous_returns = df.get("previous_returns", pd.Series(np.zeros(n))).astype(float).fillna(0.0)
    previous_refunds = df.get("previous_refunds", pd.Series(np.zeros(n))).astype(float).fillna(0.0)
    previous_rto_count = df.get("previous_rto_count", pd.Series(np.zeros(n))).astype(float).fillna(0.0)
    orders_last_7_days = df.get("orders_last_7_days", pd.Series(np.zeros(n))).astype(float).fillna(0.0)
    orders_last_30_days = df.get("orders_last_30_days", pd.Series(np.zeros(n))).astype(float).fillna(0.0)
    address_change_count = df.get("address_change_count", pd.Series(np.zeros(n))).astype(float).fillna(0.0)
    device_account_count = df.get("device_account_count", pd.Series(np.ones(n))).astype(float).fillna(1.0)
    shipping_distance_km = df.get("shipping_distance_km", pd.Series(np.zeros(n))).astype(float).fillna(250.0)
    pincode_risk_score = df.get("pincode_risk_score", pd.Series(np.zeros(n))).astype(float).fillna(0.2)
    delivery_attempts = df.get("delivery_attempts", pd.Series(np.zeros(n))).astype(float).fillna(0.0)
    is_weekend = df.get("is_weekend", pd.Series(np.zeros(n))).astype(float).fillna(0.0)
    hour_of_day = df.get("hour_of_day", pd.Series(np.full(n, 14))).astype(float).fillna(14.0)
    days_since_last_order = df.get("days_since_last_order", pd.Series(np.full(n, 30))).astype(float).fillna(30.0)
    payment_failure_count = df.get("payment_failure_count", pd.Series(np.zeros(n))).astype(float).fillna(0.0)
    previous_chargebacks = df.get("previous_chargebacks", pd.Series(np.zeros(n))).astype(float).fillna(0.0)
    historical_customer_risk = df.get("historical_customer_risk", pd.Series(np.zeros(n))).astype(float).fillna(0.1)

    safe_prev_orders = np.maximum(previous_orders.values, 1.0)
    return_rate = np.clip(previous_returns.values / safe_prev_orders, 0.0, 1.0)
    rto_rate = np.clip(previous_rto_count.values / safe_prev_orders, 0.0, 1.0)
    refund_rate = np.clip(previous_refunds.values / safe_prev_orders, 0.0, 1.0)

    account_months = np.maximum(account_age_days.values / 30.0, 0.5)
    account_activity_score = np.clip(previous_orders.values / account_months, 0.0, 15.0)
    device_reuse_score = np.maximum(device_account_count.values - 1.0, 0.0)
    address_change_frequency = np.clip(address_change_count.values / account_months, 0.0, 5.0)

    high_val = (order_value.values > 5000.0).astype(float)
    payment_methods = df.get("payment_method", pd.Series(["COD"] * n)).astype(str).fillna("COD").values
    categories = df.get("product_category", pd.Series(["Fashion & Apparel"] * n)).astype(str).fillna("Fashion & Apparel").values

    is_cod = (payment_methods == "COD").astype(float)
    high_value_cod_flag = ((order_value.values > 3000.0) & (is_cod == 1.0)).astype(float)

    payment_reliability_score = 1.0 / (1.0 + payment_failure_count.values + (previous_chargebacks.values * 2.0))

    features_df = pd.DataFrame({
        "order_value": order_value.values,
        "quantity": quantity.values,
        "account_age_days": account_age_days.values,
        "previous_orders": previous_orders.values,
        "previous_returns": previous_returns.values,
        "previous_refunds": previous_refunds.values,
        "return_rate": return_rate,
        "rto_rate": rto_rate,
        "refund_rate": refund_rate,
        "orders_per_week": orders_last_7_days.values,
        "orders_last_30_days": orders_last_30_days.values,
        "account_activity_score": account_activity_score,
        "device_reuse_score": device_reuse_score,
        "address_change_frequency": address_change_frequency,
        "high_value_order_flag": high_val,
        "high_value_cod_flag": high_value_cod_flag,
        "customer_history_score": historical_customer_risk.values,
        "pincode_risk": pincode_risk_score.values,
        "payment_reliability_score": payment_reliability_score,
        "shipping_distance_km": shipping_distance_km.values,
        "delivery_attempts": delivery_attempts.values,
        "is_weekend": is_weekend.values,
        "hour_of_day": hour_of_day.values,
        "days_since_last_order": days_since_last_order.values,
        "pay_COD": (payment_methods == "COD").astype(float),
        "pay_UPI": (payment_methods == "UPI").astype(float),
        "pay_CREDIT_CARD": (payment_methods == "CREDIT_CARD").astype(float),
        "pay_DEBIT_CARD": (payment_methods == "DEBIT_CARD").astype(float),
        "pay_NET_BANKING": (payment_methods == "NET_BANKING").astype(float),
        "cat_Electronics": (categories == "Electronics").astype(float),
        "cat_Fashion_Apparel": (categories == "Fashion & Apparel").astype(float),
        "cat_Beauty_Personal_Care": (categories == "Beauty & Personal Care").astype(float),
        "cat_Home_Kitchen": (categories == "Home & Kitchen").astype(float),
        "cat_Footwear": (categories == "Footwear").astype(float),
        "cat_Jewelry_Accessories": (categories == "Jewelry & Accessories").astype(float),
    })

    return features_df[FEATURE_COLUMNS]
