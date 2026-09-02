from typing import Dict, List, Any
import numpy as np
import pandas as pd
from ml.features import FEATURE_COLUMNS, engineer_features

FEATURE_LABELS = {
    "order_value": "Order Value (INR)",
    "quantity": "Item Quantity",
    "account_age_days": "Account Age (Tenure)",
    "previous_orders": "Completed Order Count",
    "previous_returns": "Past Returned Items",
    "previous_refunds": "Past Refunds Count",
    "return_rate": "Historical Return Ratio",
    "rto_rate": "Historical Doorstep RTO Ratio",
    "refund_rate": "Historical Refund Ratio",
    "orders_per_week": "Weekly Order Burst Velocity",
    "orders_last_30_days": "Monthly Order Velocity",
    "account_activity_score": "Account Activity Velocity",
    "device_reuse_score": "Multi-Account Device Sharing",
    "address_change_frequency": "Address Change Frequency",
    "high_value_order_flag": "High Value Ticket Size",
    "high_value_cod_flag": "High Value Cash on Delivery",
    "customer_history_score": "Customer Risk History Index",
    "pincode_risk": "Pincode Logistics Failure Risk",
    "payment_reliability_score": "Payment Reliability Score",
    "shipping_distance_km": "Logistics Transit Distance",
    "delivery_attempts": "Past Failed Delivery Attempts",
    "is_weekend": "Weekend Order Timing",
    "hour_of_day": "Order Hour Placement",
    "days_since_last_order": "Days Since Prior Order",
    "pay_COD": "Cash On Delivery Payment",
    "pay_UPI": "UPI Instant Payment (Prepaid)",
    "pay_CREDIT_CARD": "Credit Card Payment (Prepaid)",
    "pay_DEBIT_CARD": "Debit Card Payment",
    "pay_NET_BANKING": "Net Banking Payment",
    "cat_Electronics": "Category: Electronics",
    "cat_Fashion_Apparel": "Category: Fashion & Apparel",
    "cat_Beauty_Personal_Care": "Category: Beauty & Personal Care",
    "cat_Home_Kitchen": "Category: Home & Kitchen",
    "cat_Footwear": "Category: Footwear",
    "cat_Jewelry_Accessories": "Category: Jewelry & Accessories",
}

def explain_prediction(model, transaction_dict: Dict[str, Any], top_n: int = 5) -> Dict[str, Any]:
    X = engineer_features(transaction_dict)

    if hasattr(model, "booster_"):
        contribs = model.booster_.predict(X.values, pred_contrib=True)[0]
        feature_contribs = contribs[:-1]
        base_value = float(contribs[-1])
    else:
        importances = getattr(model, "feature_importances_", np.ones(len(FEATURE_COLUMNS)))
        feature_contribs = (X.values[0] - X.values[0].mean()) * (importances / (importances.sum() + 1e-6))
        base_value = 0.0

    factor_items = []
    for col_name, val in zip(FEATURE_COLUMNS, feature_contribs):
        raw_val = X.iloc[0][col_name]
        factor_items.append({
            "feature_id": col_name,
            "feature_name": FEATURE_LABELS.get(col_name, col_name),
            "raw_value": round(float(raw_val), 2),
            "contribution": round(float(val), 4),
            "impact_direction": "RISK_INCREASING" if val > 0 else "PROTECTIVE"
        })

    positive_factors = sorted(
        [f for f in factor_items if f["contribution"] > 0],
        key=lambda x: x["contribution"],
        reverse=True
    )[:top_n]

    protective_factors = sorted(
        [f for f in factor_items if f["contribution"] < 0],
        key=lambda x: x["contribution"]
    )[:top_n]

    return {
        "disclaimer": "Model contributing factors (Tree SHAP values), not causal proof.",
        "base_value": round(base_value, 4),
        "top_risk_factors": positive_factors,
        "top_protective_factors": protective_factors
    }
