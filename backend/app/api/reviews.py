from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.core.database import get_db
from backend.app.schemas.pydantic_schemas import ReviewDecisionRequest
from backend.app.models.orm_models import ReviewQueueModel, AuditLogModel, RiskPredictionModel

router = APIRouter(prefix="/api", tags=["Review Queue"])

@router.get("/reviews")
def get_review_queue(
    db: Session = Depends(get_db),
    status: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    query = db.query(ReviewQueueModel)
    if status:
        query = query.filter(ReviewQueueModel.status == status.upper())

    total = query.count()
    items = query.order_by(desc(ReviewQueueModel.created_at)).offset(offset).limit(limit).all()

    return {
        "total": total,
        "items": [
            {
                "id": r.id,
                "transaction_id": r.transaction_id,
                "customer_id": r.customer_id,
                "order_value": r.order_value,
                "risk_score": r.risk_score,
                "risk_level": r.risk_level,
                "top_risk_factor": r.top_risk_factor,
                "recommended_action": r.recommended_action,
                "status": r.status,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "updated_at": r.updated_at.isoformat() if r.updated_at else None
            }
            for r in items
        ]
    }

@router.post("/reviews/{review_id}/decision")
def submit_review_decision(
    review_id: int,
    payload: ReviewDecisionRequest,
    db: Session = Depends(get_db)
):
    review = db.query(ReviewQueueModel).filter(ReviewQueueModel.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review item not found")

    old_status = review.status
    review.status = payload.action.upper()
    review.updated_at = datetime.utcnow()

    is_override = (payload.action.upper() != review.recommended_action.upper())

    pred = db.query(RiskPredictionModel).filter(
        RiskPredictionModel.transaction_id == review.transaction_id
    ).first()

    audit_entry = AuditLogModel(
        transaction_id=review.transaction_id,
        timestamp=datetime.utcnow(),
        risk_score=review.risk_score,
        risk_level=review.risk_level,
        model_version="1.0.0",
        recommended_action=review.recommended_action,
        decision_status=f"HUMAN_{payload.action.upper()}",
        risk_factors=pred.top_risk_factors if pred else [],
        decision_reason=payload.reason or f"Status changed from {old_status} to {payload.action}",
        human_override=is_override,
        final_action=payload.action.upper(),
        operator_name=payload.operator_name or "Human Risk Analyst"
    )

    db.add(audit_entry)
    db.commit()
    db.refresh(review)

    return {
        "message": "Decision recorded successfully",
        "review_id": review.id,
        "transaction_id": review.transaction_id,
        "new_status": review.status,
        "human_override": is_override,
        "audit_logged": True
    }
