from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.core.database import get_db
from backend.app.models.orm_models import TransactionModel, RiskPredictionModel, ReviewQueueModel

router = APIRouter(prefix="/api", tags=["Dashboard"])

@router.get("/dashboard")
def get_dashboard_summary(db: Session = Depends(get_db)):
    total_txns = db.query(func.count(TransactionModel.id)).scalar() or 0
    total_volume = db.query(func.sum(TransactionModel.order_value)).scalar() or 0.0

    high_risk_count = db.query(func.count(RiskPredictionModel.id)).filter(
        RiskPredictionModel.risk_level == "HIGH"
    ).scalar() or 0

    med_risk_count = db.query(func.count(RiskPredictionModel.id)).filter(
        RiskPredictionModel.risk_level == "MEDIUM"
    ).scalar() or 0

    low_risk_count = db.query(func.count(RiskPredictionModel.id)).filter(
        RiskPredictionModel.risk_level == "LOW"
    ).scalar() or 0

    total_estimated_loss = db.query(func.sum(RiskPredictionModel.estimated_loss)).filter(
        RiskPredictionModel.risk_level.in_(["HIGH", "MEDIUM"])
    ).scalar() or 0.0

    total_prevented_loss = db.query(func.sum(RiskPredictionModel.expected_benefit)).scalar() or 0.0
    pending_reviews_count = db.query(func.count(ReviewQueueModel.id)).filter(
        ReviewQueueModel.status == "PENDING"
    ).scalar() or 0

    category_data = db.query(
        TransactionModel.product_category,
        func.count(TransactionModel.id).label("total_orders"),
        func.avg(RiskPredictionModel.risk_score).label("avg_risk_score"),
        func.sum(TransactionModel.order_value).label("total_amount")
    ).outerjoin(
        RiskPredictionModel, TransactionModel.transaction_id == RiskPredictionModel.transaction_id
    ).group_by(TransactionModel.product_category).all()

    category_breakdown = [
        {
            "category": c[0],
            "total_orders": c[1],
            "avg_risk_score": round(float(c[2] or 0), 1),
            "total_amount": round(float(c[3] or 0), 2)
        }
        for c in category_data
    ]

    payment_data = db.query(
        TransactionModel.payment_method,
        func.count(TransactionModel.id).label("total_orders"),
        func.avg(RiskPredictionModel.risk_score).label("avg_risk_score")
    ).outerjoin(
        RiskPredictionModel, TransactionModel.transaction_id == RiskPredictionModel.transaction_id
    ).group_by(TransactionModel.payment_method).all()

    payment_breakdown = [
        {
            "payment_method": p[0],
            "total_orders": p[1],
            "avg_risk_score": round(float(p[2] or 0), 1)
        }
        for p in payment_data
    ]

    risk_distribution = [
        {"name": "Low Risk (0-30)", "value": low_risk_count, "color": "#10B981"},
        {"name": "Medium Risk (31-70)", "value": med_risk_count, "color": "#F59E0B"},
        {"name": "High Risk (71-100)", "value": high_risk_count, "color": "#EF4444"}
    ]

    return {
        "overview": {
            "total_transactions": total_txns,
            "total_volume_inr": round(float(total_volume), 2),
            "high_risk_count": high_risk_count,
            "medium_risk_count": med_risk_count,
            "low_risk_count": low_risk_count,
            "total_estimated_loss": round(float(total_estimated_loss), 2),
            "total_prevented_loss": round(float(total_prevented_loss), 2),
            "pending_reviews": pending_reviews_count,
            "avg_risk_rate_pct": round((high_risk_count + med_risk_count) / max(total_txns, 1) * 100, 2)
        },
        "risk_distribution": risk_distribution,
        "category_breakdown": category_breakdown,
        "payment_breakdown": payment_breakdown
    }
