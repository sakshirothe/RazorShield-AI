from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.orm_models import MerchantSettingsModel
from backend.app.schemas.pydantic_schemas import MerchantSettingsSchema

router = APIRouter(prefix="/api", tags=["Settings"])

@router.get("/settings", response_model=MerchantSettingsSchema)
def get_merchant_settings(db: Session = Depends(get_db)):
    settings_obj = db.query(MerchantSettingsModel).filter(
        MerchantSettingsModel.merchant_id == "DEFAULT"
    ).first()

    if not settings_obj:
        settings_obj = MerchantSettingsModel(merchant_id="DEFAULT")
        db.add(settings_obj)
        db.commit()
        db.refresh(settings_obj)

    return MerchantSettingsSchema(
        merchant_id=settings_obj.merchant_id,
        low_threshold=settings_obj.low_threshold,
        medium_threshold=settings_obj.medium_threshold,
        verification_cost=settings_obj.verification_cost,
        manual_review_cost=settings_obj.manual_review_cost,
        false_positive_cost=settings_obj.false_positive_cost,
        average_loss_per_risky_order=settings_obj.average_loss_per_risky_order,
        auto_approve_low_risk=settings_obj.auto_approve_low_risk
    )

@router.post("/settings", response_model=MerchantSettingsSchema)
def update_merchant_settings(payload: MerchantSettingsSchema, db: Session = Depends(get_db)):
    settings_obj = db.query(MerchantSettingsModel).filter(
        MerchantSettingsModel.merchant_id == payload.merchant_id
    ).first()

    if not settings_obj:
        settings_obj = MerchantSettingsModel(merchant_id=payload.merchant_id)
        db.add(settings_obj)

    settings_obj.low_threshold = payload.low_threshold
    settings_obj.medium_threshold = payload.medium_threshold
    settings_obj.verification_cost = payload.verification_cost
    settings_obj.manual_review_cost = payload.manual_review_cost
    settings_obj.false_positive_cost = payload.false_positive_cost
    settings_obj.average_loss_per_risky_order = payload.average_loss_per_risky_order
    settings_obj.auto_approve_low_risk = payload.auto_approve_low_risk

    db.commit()
    db.refresh(settings_obj)

    return payload
