import pandas as pd
from ml.features import engineer_features, FEATURE_COLUMNS

def test_feature_columns_and_shape():
    raw_sample = {
        "order_value": 2499.0,
        "payment_method": "COD",
        "product_category": "Fashion & Apparel",
        "quantity": 2,
        "account_age_days": 120,
        "previous_orders": 5,
        "previous_returns": 1,
        "previous_refunds": 1,
        "previous_rto_count": 1,
        "days_since_last_order": 14,
        "orders_last_7_days": 1,
        "orders_last_30_days": 3,
        "address_change_count": 0,
        "device_account_count": 1,
        "shipping_distance_km": 400.0,
        "pincode_risk_score": 0.35,
        "delivery_attempts": 0,
        "payment_failure_count": 0,
        "previous_chargebacks": 0,
        "historical_customer_risk": 0.15
    }

    df = engineer_features(raw_sample)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert list(df.columns) == FEATURE_COLUMNS

def test_derived_features_math():
    raw_sample = {
        "order_value": 6000.0,
        "payment_method": "COD",
        "account_age_days": 60,
        "previous_orders": 10,
        "previous_returns": 4,
        "previous_rto_count": 2,
        "device_account_count": 3
    }
    df = engineer_features(raw_sample)
    assert df["return_rate"].iloc[0] == 0.4
    assert df["rto_rate"].iloc[0] == 0.2
    assert df["high_value_order_flag"].iloc[0] == 1.0
    assert df["high_value_cod_flag"].iloc[0] == 1.0
    assert df["device_reuse_score"].iloc[0] == 2.0
    assert df["pay_COD"].iloc[0] == 1.0
    assert df["pay_UPI"].iloc[0] == 0.0

def test_missing_and_zero_safety():
    df = engineer_features({})
    assert len(df) == 1
    assert not df.isnull().values.any()
