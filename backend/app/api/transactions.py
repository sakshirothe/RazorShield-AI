from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.core.database import get_db
from backend.app.models.orm_models import TransactionModel, RiskPredictionModel, ReviewQueueModel

router = APIRouter(prefix="/api", tags=["Transactions"])

@router.get("/transactions")
def get_transactions(
    db: Session = Depends(get_db),
    limit: int = Query(25, ge=1, le=100),
    offset: int = Query(0, ge=0),
    risk_level: Optional[str] = None,
    payment_method: Optional[str] = None,
    search: Optional[str] = None
):
    query = db.query(TransactionModel, RiskPredictionModel).outerjoin(
        RiskPredictionModel, TransactionModel.transaction_id == RiskPredictionModel.transaction_id
    )

    if risk_level:
        query = query.filter(RiskPredictionModel.risk_level == risk_level.upper())

    if payment_method:
        query = query.filter(TransactionModel.payment_method == payment_method.upper())

    if search:
        query = query.filter(
            (TransactionModel.transaction_id.ilike(f"%{search}%")) |
            (TransactionModel.customer_id.ilike(f"%{search}%"))
        )

    total_count = query.count()
    results = query.order_by(desc(TransactionModel.created_at)).offset(offset).limit(limit).all()

    items = []
    for txn, pred in results:
        items.append({
            "transaction_id": txn.transaction_id,
            "customer_id": txn.customer_id,
            "merchant_id": txn.merchant_id,
            "order_value": txn.order_value,
            "payment_method": txn.payment_method,
            "product_category": txn.product_category,
            "account_age_days": txn.account_age_days,
            "previous_returns": txn.previous_returns,
            "previous_orders": txn.previous_orders,
            "created_at": txn.created_at.isoformat() if txn.created_at else None,
            "risk_score": pred.risk_score if pred else None,
            "risk_level": pred.risk_level if pred else "UNCLASSIFIED",
            "recommended_action": pred.recommended_action if pred else "NONE",
            "estimated_loss": pred.estimated_loss if pred else 0.0,
            "expected_benefit": pred.expected_benefit if pred else 0.0
        })

    return {
        "total": total_count,
        "limit": limit,
        "offset": offset,
        "items": items
    }

@router.get("/transactions/{transaction_id}")
def get_transaction_detail(
    transaction_id: str,
    db: Session = Depends(get_db)
):
    txn = db.query(TransactionModel).filter(TransactionModel.transaction_id == transaction_id).first()
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")

    pred = db.query(RiskPredictionModel).filter(RiskPredictionModel.transaction_id == transaction_id).first()
    rev = db.query(ReviewQueueModel).filter(ReviewQueueModel.transaction_id == transaction_id).first()

    return {
        "transaction": {
            "transaction_id": txn.transaction_id,
            "customer_id": txn.customer_id,
            "merchant_id": txn.merchant_id,
            "order_value": txn.order_value,
            "payment_method": txn.payment_method,
            "product_category": txn.product_category,
            "quantity": txn.quantity,
            "account_age_days": txn.account_age_days,
            "previous_orders": txn.previous_orders,
            "previous_returns": txn.previous_returns,
            "previous_refunds": txn.previous_refunds,
            "return_rate": txn.return_rate,
            "rto_rate": txn.rto_rate,
            "device_account_count": txn.device_account_count,
            "address_change_count": txn.address_change_count,
            "shipping_distance_km": txn.shipping_distance_km,
            "pincode_risk_score": txn.pincode_risk_score,
            "delivery_attempts": txn.delivery_attempts,
            "created_at": txn.created_at.isoformat() if txn.created_at else None
        },
        "prediction": {
            "risk_score": pred.risk_score if pred else None,
            "risk_probability": pred.risk_probability if pred else None,
            "risk_level": pred.risk_level if pred else "UNCLASSIFIED",
            "recommended_action": pred.recommended_action if pred else "NONE",
            "estimated_loss": pred.estimated_loss if pred else 0.0,
            "intervention_cost": pred.intervention_cost if pred else 0.0,
            "expected_benefit": pred.expected_benefit if pred else 0.0,
            "decision_reason": pred.decision_reason if pred else None,
            "top_risk_factors": pred.top_risk_factors if pred else [],
            "top_protective_factors": pred.top_protective_factors if pred else [],
            "ai_explanation": pred.ai_explanation if pred else None
        } if pred else None,
        "review_status": rev.status if rev else "NOT_QUEUED"
    }
