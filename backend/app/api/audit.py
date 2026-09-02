from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.core.database import get_db
from backend.app.models.orm_models import AuditLogModel

router = APIRouter(prefix="/api", tags=["Audit Log"])

@router.get("/audit")
def get_audit_logs(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    human_override_only: Optional[bool] = None,
    search: Optional[str] = None
):
    query = db.query(AuditLogModel)

    if human_override_only is not None:
        query = query.filter(AuditLogModel.human_override == human_override_only)

    if search:
        query = query.filter(AuditLogModel.transaction_id.ilike(f"%{search}%"))

    total = query.count()
    items = query.order_by(desc(AuditLogModel.timestamp)).offset(offset).limit(limit).all()

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": [
            {
                "id": log.id,
                "transaction_id": log.transaction_id,
                "timestamp": log.timestamp.isoformat() if log.timestamp else None,
                "risk_score": log.risk_score,
                "risk_level": log.risk_level,
                "model_version": log.model_version,
                "recommended_action": log.recommended_action,
                "decision_status": log.decision_status,
                "risk_factors": log.risk_factors,
                "decision_reason": log.decision_reason,
                "human_override": log.human_override,
                "final_action": log.final_action,
                "operator_name": log.operator_name
            }
            for log in items
        ]
    }
