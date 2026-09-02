import os
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session

from backend.app.models.orm_models import (
    TransactionModel, RiskPredictionModel, ReviewQueueModel, AuditLogModel, MerchantSettingsModel
)
from backend.app.services.ml_predictor import risk_predictor

DEMO_SCENARIOS = [
    {
        "transaction_id": "DEMO_SCENARIO_1",
        "customer_id": "CUST_LOYAL_01",
        "merchant_id": "MERCH_001",
        "order_value": 1499.0,
        "payment_method": "UPI",
        "product_category": "Fashion & Apparel",
        "quantity": 1,
        "account_age_days": 420,
        "previous_orders": 24,
        "previous_returns": 1,
        "previous_refunds": 1,
        "previous_rto_count": 0,
        "days_since_last_order": 12,
        "orders_last_7_days": 1,
        "orders_last_30_days": 3,
        "address_change_count": 0,
        "device_account_count": 1,
        "shipping_distance_km": 180.0,
        "pincode_risk_score": 0.12,
        "delivery_attempts": 0,
        "payment_failure_count": 0,
        "previous_chargebacks": 0,
        "historical_customer_risk": 0.04,
        "scenario_title": "Scenario 1: Low-Risk Loyal Customer (Seamless Approval)"
    },
    {
        "transaction_id": "DEMO_SCENARIO_2",
        "customer_id": "CUST_MOD_02",
        "merchant_id": "MERCH_001",
        "order_value": 2899.0,
        "payment_method": "COD",
        "product_category": "Footwear",
        "quantity": 1,
        "account_age_days": 65,
        "previous_orders": 4,
        "previous_returns": 1,
        "previous_refunds": 1,
        "previous_rto_count": 0,
        "days_since_last_order": 28,
        "orders_last_7_days": 1,
        "orders_last_30_days": 2,
        "address_change_count": 1,
        "device_account_count": 1,
        "shipping_distance_km": 650.0,
        "pincode_risk_score": 0.45,
        "delivery_attempts": 1,
        "payment_failure_count": 1,
        "previous_chargebacks": 0,
        "historical_customer_risk": 0.28,
        "scenario_title": "Scenario 2: Medium-Risk Order (Additional Verification Recommended)"
    },
    {
        "transaction_id": "DEMO_SCENARIO_3",
        "customer_id": "CUST_ABUSER_03",
        "merchant_id": "MERCH_001",
        "order_value": 6499.0,
        "payment_method": "COD",
        "product_category": "Electronics",
        "quantity": 2,
        "account_age_days": 4,
        "previous_orders": 3,
        "previous_returns": 2,
        "previous_refunds": 2,
        "previous_rto_count": 2,
        "days_since_last_order": 2,
        "orders_last_7_days": 4,
        "orders_last_30_days": 4,
        "address_change_count": 3,
        "device_account_count": 4,
        "shipping_distance_km": 1600.0,
        "pincode_risk_score": 0.78,
        "delivery_attempts": 2,
        "payment_failure_count": 3,
        "previous_chargebacks": 1,
        "historical_customer_risk": 0.75,
        "scenario_title": "Scenario 3: High-Risk Multi-Account RTO Cluster (Manual Review)"
    },
    {
        "transaction_id": "DEMO_SCENARIO_4",
        "customer_id": "CUST_BURST_04",
        "merchant_id": "MERCH_001",
        "order_value": 18500.0,
        "payment_method": "COD",
        "product_category": "Jewelry & Accessories",
        "quantity": 3,
        "account_age_days": 2,
        "previous_orders": 0,
        "previous_returns": 0,
        "previous_refunds": 0,
        "previous_rto_count": 0,
        "days_since_last_order": 2,
        "orders_last_7_days": 5,
        "orders_last_30_days": 5,
        "address_change_count": 2,
        "device_account_count": 3,
        "shipping_distance_km": 2100.0,
        "pincode_risk_score": 0.82,
        "delivery_attempts": 0,
        "payment_failure_count": 2,
        "previous_chargebacks": 0,
        "historical_customer_risk": 0.65,
        "scenario_title": "Scenario 4: High-Value COD Velocity Spike (Significant Potential Loss)"
    },
    {
        "transaction_id": "DEMO_SCENARIO_5",
        "customer_id": "CUST_FP_05",
        "merchant_id": "MERCH_001",
        "order_value": 12000.0,
        "payment_method": "CREDIT_CARD",
        "product_category": "Electronics",
        "quantity": 1,
        "account_age_days": 18,
        "previous_orders": 1,
        "previous_returns": 0,
        "previous_refunds": 0,
        "previous_rto_count": 0,
        "days_since_last_order": 14,
        "orders_last_7_days": 1,
        "orders_last_30_days": 1,
        "address_change_count": 1,
        "device_account_count": 1,
        "shipping_distance_km": 1400.0,
        "pincode_risk_score": 0.55,
        "delivery_attempts": 0,
        "payment_failure_count": 0,
        "previous_chargebacks": 0,
        "historical_customer_risk": 0.15,
        "scenario_title": "Scenario 5: False-Positive Candidate (High-Value Prepaid Gift)"
    }
]

def seed_database_if_empty(db: Session, csv_path: str = "data/transactions.csv", n_seed: int = 30):
    existing_count = db.query(TransactionModel).count()
    if existing_count > 0:
        return

    settings_obj = db.query(MerchantSettingsModel).filter(MerchantSettingsModel.merchant_id == "DEFAULT").first()
    if not settings_obj:
        settings_obj = MerchantSettingsModel(merchant_id="DEFAULT")
        db.add(settings_obj)
        db.commit()

    for s in DEMO_SCENARIOS:
        s_copy = dict(s)
        s_copy.pop("scenario_title", "")
        txn_id = s_copy["transaction_id"]

        txn_record = TransactionModel(
            transaction_id=txn_id,
            customer_id=s_copy["customer_id"],
            merchant_id=s_copy["merchant_id"],
            order_value=s_copy["order_value"],
            payment_method=s_copy["payment_method"],
            product_category=s_copy["product_category"],
            quantity=s_copy["quantity"],
            account_age_days=s_copy["account_age_days"],
            previous_orders=s_copy["previous_orders"],
            previous_returns=s_copy["previous_returns"],
            previous_refunds=s_copy["previous_refunds"],
            return_rate=round(s_copy["previous_returns"] / max(s_copy["previous_orders"], 1), 4),
            rto_rate=round(s_copy["previous_rto_count"] / max(s_copy["previous_orders"], 1), 4),
            days_since_last_order=s_copy["days_since_last_order"],
            orders_last_7_days=s_copy["orders_last_7_days"],
            orders_last_30_days=s_copy["orders_last_30_days"],
            address_change_count=s_copy["address_change_count"],
            device_account_count=s_copy["device_account_count"],
            shipping_distance_km=s_copy["shipping_distance_km"],
            pincode_risk_score=s_copy["pincode_risk_score"],
            delivery_attempts=s_copy["delivery_attempts"],
            historical_customer_risk=s_copy["historical_customer_risk"],
            payment_failure_count=s_copy["payment_failure_count"],
            previous_chargebacks=s_copy["previous_chargebacks"],
            previous_rto_count=s_copy["previous_rto_count"],
            created_at=datetime.utcnow()
        )
        db.add(txn_record)

        res = risk_predictor.predict_transaction(s_copy)
        dec = res["decision"]
        top_risk = res["top_risk_factors"]
        top_prot = res["top_protective_factors"]

        pred_record = RiskPredictionModel(
            transaction_id=txn_id,
            risk_score=dec["risk_score"],
            risk_probability=dec["risk_probability"],
            risk_level=dec["risk_level"],
            recommended_action=dec["recommended_action"],
            estimated_loss=dec["estimated_loss"],
            intervention_cost=dec["intervention_cost"],
            expected_benefit=dec["expected_benefit"],
            decision_reason=dec["reason"],
            top_risk_factors=top_risk,
            top_protective_factors=top_prot,
            ai_explanation=res["ai_risk_assessment"]
        )
        db.add(pred_record)

        if dec["risk_level"] in ["MEDIUM", "HIGH"]:
            top_factor_name = top_risk[0]["feature_name"] if top_risk else "Risk Threshold"
            rev_record = ReviewQueueModel(
                transaction_id=txn_id,
                customer_id=s_copy["customer_id"],
                order_value=s_copy["order_value"],
                risk_score=dec["risk_score"],
                risk_level=dec["risk_level"],
                top_risk_factor=top_factor_name,
                recommended_action=dec["recommended_action"],
                status="PENDING"
            )
            db.add(rev_record)

        audit_record = AuditLogModel(
            transaction_id=txn_id,
            timestamp=datetime.utcnow(),
            risk_score=dec["risk_score"],
            risk_level=dec["risk_level"],
            model_version="1.0.0",
            recommended_action=dec["recommended_action"],
            decision_status="AI_RECOMMENDED",
            risk_factors=top_risk,
            decision_reason=dec["reason"],
            human_override=False,
            final_action=dec["recommended_action"],
            operator_name="RazorShield Engine"
        )
        db.add(audit_record)

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path, nrows=n_seed)
        for _, row in df.iterrows():
            row_dict = row.to_dict()
            txn_id = str(row_dict["transaction_id"])
            if db.query(TransactionModel).filter(TransactionModel.transaction_id == txn_id).first():
                continue

            txn_record = TransactionModel(
                transaction_id=txn_id,
                customer_id=str(row_dict.get("customer_id", "CUST_000")),
                merchant_id=str(row_dict.get("merchant_id", "MERCH_001")),
                order_value=float(row_dict.get("order_value", 1000.0)),
                payment_method=str(row_dict.get("payment_method", "COD")),
                product_category=str(row_dict.get("product_category", "Fashion & Apparel")),
                quantity=int(row_dict.get("quantity", 1)),
                account_age_days=int(row_dict.get("account_age_days", 30)),
                previous_orders=int(row_dict.get("previous_orders", 0)),
                previous_returns=int(row_dict.get("previous_returns", 0)),
                previous_refunds=int(row_dict.get("previous_refunds", 0)),
                return_rate=float(row_dict.get("return_rate", 0.0)),
                rto_rate=float(row_dict.get("rto_rate", 0.0)),
                days_since_last_order=int(row_dict.get("days_since_last_order", 30)),
                orders_last_7_days=int(row_dict.get("orders_last_7_days", 0)),
                orders_last_30_days=int(row_dict.get("orders_last_30_days", 0)),
                address_change_count=int(row_dict.get("address_change_count", 0)),
                device_account_count=int(row_dict.get("device_account_count", 1)),
                shipping_distance_km=float(row_dict.get("shipping_distance_km", 250.0)),
                pincode_risk_score=float(row_dict.get("pincode_risk_score", 0.2)),
                delivery_attempts=int(row_dict.get("delivery_attempts", 0)),
                historical_customer_risk=float(row_dict.get("historical_customer_risk", 0.1)),
                payment_failure_count=int(row_dict.get("payment_failure_count", 0)),
                previous_chargebacks=int(row_dict.get("previous_chargebacks", 0)),
                previous_rto_count=int(row_dict.get("previous_rto_count", 0)),
                label=int(row_dict.get("label", 0)),
                created_at=datetime.utcnow()
            )
            db.add(txn_record)

            res = risk_predictor.predict_transaction(row_dict)
            dec = res["decision"]
            top_risk = res["top_risk_factors"]
            top_prot = res["top_protective_factors"]

            pred_record = RiskPredictionModel(
                transaction_id=txn_id,
                risk_score=dec["risk_score"],
                risk_probability=dec["risk_probability"],
                risk_level=dec["risk_level"],
                recommended_action=dec["recommended_action"],
                estimated_loss=dec["estimated_loss"],
                intervention_cost=dec["intervention_cost"],
                expected_benefit=dec["expected_benefit"],
                decision_reason=dec["reason"],
                top_risk_factors=top_risk,
                top_protective_factors=top_prot,
                ai_explanation=res["ai_risk_assessment"]
            )
            db.add(pred_record)

            if dec["risk_level"] in ["MEDIUM", "HIGH"]:
                top_factor_name = top_risk[0]["feature_name"] if top_risk else "Risk Factor"
                rev_record = ReviewQueueModel(
                    transaction_id=txn_id,
                    customer_id=str(row_dict.get("customer_id", "CUST_000")),
                    order_value=float(row_dict.get("order_value", 1000.0)),
                    risk_score=dec["risk_score"],
                    risk_level=dec["risk_level"],
                    top_risk_factor=top_factor_name,
                    recommended_action=dec["recommended_action"],
                    status="PENDING"
                )
                db.add(rev_record)

    db.commit()
