from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class TransactionInput(BaseModel):
    transaction_id: Optional[str] = None
    customer_id: Optional[str] = "CUST_999999"
    merchant_id: Optional[str] = "MERCH_001"
    order_value: float = Field(..., gt=0)
    payment_method: str = Field(...)
    product_category: str = Field(...)
    quantity: int = Field(default=1, ge=1)
    account_age_days: int = Field(default=30, ge=0)
    previous_orders: int = Field(default=0, ge=0)
    previous_returns: int = Field(default=0, ge=0)
    previous_refunds: int = Field(default=0, ge=0)
    previous_rto_count: int = Field(default=0, ge=0)
    days_since_last_order: int = Field(default=15, ge=0)
    orders_last_7_days: int = Field(default=0, ge=0)
    orders_last_30_days: int = Field(default=0, ge=0)
    address_change_count: int = Field(default=0, ge=0)
    device_account_count: int = Field(default=1, ge=1)
    shipping_distance_km: float = Field(default=350.0, ge=0.0)
    pincode_risk_score: float = Field(default=0.25, ge=0.0, le=1.0)
    delivery_attempts: int = Field(default=0, ge=0)
    payment_failure_count: int = Field(default=0, ge=0)
    previous_chargebacks: int = Field(default=0, ge=0)
    historical_customer_risk: Optional[float] = 0.1
    is_weekend: Optional[int] = 0
    hour_of_day: Optional[int] = 14

class SimulationInput(BaseModel):
    base_transaction: Optional[TransactionInput] = None
    order_value: float
    payment_method: str
    product_category: str = "Fashion & Apparel"
    account_age_days: int
    previous_orders: int
    previous_returns: int
    previous_rto_count: int = 0
    address_change_count: int
    device_account_count: int
    pincode_risk_score: float
    shipping_distance_km: float = 300.0

class RiskFactorItem(BaseModel):
    feature_id: str
    feature_name: str
    raw_value: float
    contribution: float
    impact_direction: str

class DecisionResult(BaseModel):
    risk_score: int
    risk_probability: float
    risk_level: str
    recommended_action: str
    estimated_loss: float
    intervention_cost: float
    expected_benefit: float
    reason: str

class AnalyzeResponse(BaseModel):
    transaction_id: str
    decision: DecisionResult
    top_risk_factors: List[RiskFactorItem]
    top_protective_factors: List[RiskFactorItem]
    ai_risk_assessment: str
    metadata: Dict[str, Any]

class ReviewDecisionRequest(BaseModel):
    action: str = Field(...)
    reason: Optional[str] = "Approved after merchant review"
    operator_name: Optional[str] = "Merchant Admin"

class AuditLogItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    transaction_id: str
    timestamp: datetime
    risk_score: int
    risk_level: str
    model_version: str
    recommended_action: str
    decision_status: str
    risk_factors: Optional[List[Dict[str, Any]]] = None
    decision_reason: Optional[str] = None
    human_override: bool
    final_action: str
    operator_name: str

class MerchantSettingsSchema(BaseModel):
    merchant_id: str = "DEFAULT"
    low_threshold: int = 30
    medium_threshold: int = 70
    verification_cost: float = 25.0
    manual_review_cost: float = 65.0
    false_positive_cost: float = 220.0
    average_loss_per_risky_order: float = 2400.0
    auto_approve_low_risk: bool = True
