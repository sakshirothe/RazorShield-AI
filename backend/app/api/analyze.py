import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.schemas.pydantic_schemas import TransactionInput, AnalyzeResponse
from backend.app.services.ml_predictor import risk_predictor
from backend.app.models.orm_models import (
    TransactionModel, RiskPredictionModel, ReviewQueueModel, AuditLogModel, MerchantSettingsModel
)

router = APIRouter(prefix="/api", tags=["Risk Analysis"])

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_transaction(
    payload: TransactionInput,
    db: Session = Depends(get_db)
):
    txn_id = payload.transaction_id or f"RZ_{uuid.uuid4().hex[:8].upper()}"
    data = payload.model_dump()
    data["transaction_id"] = txn_id

    merchant_settings = db.query(MerchantSettingsModel).filter(
        MerchantSettingsModel.merchant_id == payload.merchant_id
    ).first()

    settings_dict = {}
    if merchant_settings:
        settings_dict = {
            "low_threshold": merchant_settings.low_threshold,
            "medium_threshold": merchant_settings.medium_threshold,
            "verification_cost": merchant_settings.verification_cost,
            "manual_review_cost": merchant_settings.manual_review_cost,
            "false_positive_cost": merchant_settings.false_positive_cost,
            "average_loss_per_risky_order": merchant_settings.average_loss_per_risky_order,
        }

    try:
        result = risk_predictor.predict_transaction(data, settings_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

    decision = result["decision"]
    top_risk = result["top_risk_factors"]
    top_prot = result["top_protective_factors"]
    ai_assessment = result["ai_risk_assessment"]

    existing_txn = db.query(TransactionModel).filter(TransactionModel.transaction_id == txn_id).first()
    if not existing_txn:
        txn_record = TransactionModel(
            transaction_id=txn_id,
            customer_id=payload.customer_id,
            merchant_id=payload.merchant_id,
            order_value=payload.order_value,
            payment_method=payload.payment_method,
            product_category=payload.product_category,
            quantity=payload.quantity,
            account_age_days=payload.account_age_days,
            previous_orders=payload.previous_orders,
            previous_returns=payload.previous_returns,
            previous_refunds=payload.previous_refunds,
            return_rate=round(payload.previous_returns / max(payload.previous_orders, 1), 4),
            rto_rate=round(payload.previous_rto_count / max(payload.previous_orders, 1), 4),
            days_since_last_order=payload.days_since_last_order,
            orders_last_7_days=payload.orders_last_7_days,
            orders_last_30_days=payload.orders_last_30_days,
            address_change_count=payload.address_change_count,
            device_account_count=payload.device_account_count,
            shipping_distance_km=payload.shipping_distance_km,
            pincode_risk_score=payload.pincode_risk_score,
            delivery_attempts=payload.delivery_attempts,
            historical_customer_risk=payload.historical_customer_risk or 0.1,
            is_weekend=payload.is_weekend,
            hour_of_day=payload.hour_of_day,
            payment_failure_count=payload.payment_failure_count,
            previous_chargebacks=payload.previous_chargebacks,
            previous_rto_count=payload.previous_rto_count
        )
        db.add(txn_record)
        db.flush()

    existing_pred = db.query(RiskPredictionModel).filter(RiskPredictionModel.transaction_id == txn_id).first()
    if existing_pred:
        existing_pred.risk_score = decision["risk_score"]
        existing_pred.risk_probability = decision["risk_probability"]
        existing_pred.risk_level = decision["risk_level"]
        existing_pred.recommended_action = decision["recommended_action"]
        existing_pred.estimated_loss = decision["estimated_loss"]
        existing_pred.intervention_cost = decision["intervention_cost"]
        existing_pred.expected_benefit = decision["expected_benefit"]
        existing_pred.decision_reason = decision["reason"]
        existing_pred.top_risk_factors = top_risk
        existing_pred.top_protective_factors = top_prot
        existing_pred.ai_explanation = ai_assessment
    else:
        pred_record = RiskPredictionModel(
            transaction_id=txn_id,
            risk_score=decision["risk_score"],
            risk_probability=decision["risk_probability"],
            risk_level=decision["risk_level"],
            recommended_action=decision["recommended_action"],
            estimated_loss=decision["estimated_loss"],
            intervention_cost=decision["intervention_cost"],
            expected_benefit=decision["expected_benefit"],
            decision_reason=decision["reason"],
            top_risk_factors=top_risk,
            top_protective_factors=top_prot,
            ai_explanation=ai_assessment
        )
        db.add(pred_record)

    if decision["risk_level"] in ["MEDIUM", "HIGH"]:
        existing_rev = db.query(ReviewQueueModel).filter(ReviewQueueModel.transaction_id == txn_id).first()
        primary_factor = top_risk[0]["feature_name"] if top_risk else "Risk Threshold Flag"
        if not existing_rev:
            rev_record = ReviewQueueModel(
                transaction_id=txn_id,
                customer_id=payload.customer_id,
                order_value=payload.order_value,
                risk_score=decision["risk_score"],
                risk_level=decision["risk_level"],
                top_risk_factor=primary_factor,
                recommended_action=decision["recommended_action"],
                status="PENDING"
            )
            db.add(rev_record)

    audit_record = AuditLogModel(
        transaction_id=txn_id,
        timestamp=datetime.utcnow(),
        risk_score=decision["risk_score"],
        risk_level=decision["risk_level"],
        model_version="1.0.0",
        recommended_action=decision["recommended_action"],
        decision_status="AI_RECOMMENDED",
        risk_factors=top_risk,
        decision_reason=decision["reason"],
        human_override=False,
        final_action=decision["recommended_action"],
        operator_name="RazorShield Engine"
    )
    db.add(audit_record)
    db.commit()

    return AnalyzeResponse(
        transaction_id=txn_id,
        decision=decision,
        top_risk_factors=top_risk,
        top_protective_factors=top_prot,
        ai_risk_assessment=ai_assessment,
        metadata=result["metadata"]
    )
