from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey
)
from sqlalchemy.orm import relationship

from backend.app.core.database import Base

class TransactionModel(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(64), unique=True, index=True, nullable=False)
    customer_id = Column(String(64), index=True, nullable=False)
    merchant_id = Column(String(64), index=True, nullable=False)
    order_value = Column(Float, nullable=False)
    payment_method = Column(String(32), nullable=False)
    product_category = Column(String(64), nullable=False)
    quantity = Column(Integer, default=1)
    account_age_days = Column(Integer, default=0)
    previous_orders = Column(Integer, default=0)
    previous_returns = Column(Integer, default=0)
    previous_refunds = Column(Integer, default=0)
    return_rate = Column(Float, default=0.0)
    rto_rate = Column(Float, default=0.0)
    days_since_last_order = Column(Integer, default=30)
    orders_last_7_days = Column(Integer, default=0)
    orders_last_30_days = Column(Integer, default=0)
    address_change_count = Column(Integer, default=0)
    device_account_count = Column(Integer, default=1)
    shipping_distance_km = Column(Float, default=200.0)
    pincode_risk_score = Column(Float, default=0.2)
    delivery_attempts = Column(Integer, default=0)
    historical_customer_risk = Column(Float, default=0.1)
    is_weekend = Column(Integer, default=0)
    hour_of_day = Column(Integer, default=14)
    customer_order_frequency = Column(Float, default=0.0)
    payment_failure_count = Column(Integer, default=0)
    previous_chargebacks = Column(Integer, default=0)
    previous_rto_count = Column(Integer, default=0)
    label = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    prediction = relationship("RiskPredictionModel", back_populates="transaction", uselist=False)
    review_item = relationship("ReviewQueueModel", back_populates="transaction", uselist=False)

class RiskPredictionModel(Base):
    __tablename__ = "risk_predictions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(64), ForeignKey("transactions.transaction_id"), unique=True, index=True, nullable=False)
    risk_score = Column(Integer, nullable=False)
    risk_probability = Column(Float, nullable=False)
    risk_level = Column(String(16), nullable=False)
    recommended_action = Column(String(32), nullable=False)
    estimated_loss = Column(Float, nullable=False)
    intervention_cost = Column(Float, nullable=False)
    expected_benefit = Column(Float, nullable=False)
    decision_reason = Column(Text, nullable=True)
    top_risk_factors = Column(JSON, nullable=True)
    top_protective_factors = Column(JSON, nullable=True)
    ai_explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    transaction = relationship("TransactionModel", back_populates="prediction")

class ReviewQueueModel(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(64), ForeignKey("transactions.transaction_id"), unique=True, index=True, nullable=False)
    customer_id = Column(String(64), nullable=False)
    order_value = Column(Float, nullable=False)
    risk_score = Column(Integer, nullable=False)
    risk_level = Column(String(16), nullable=False)
    top_risk_factor = Column(String(128), nullable=True)
    recommended_action = Column(String(32), nullable=False)
    status = Column(String(32), default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    transaction = relationship("TransactionModel", back_populates="review_item")

class AuditLogModel(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(64), index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    risk_score = Column(Integer, nullable=False)
    risk_level = Column(String(16), nullable=False)
    model_version = Column(String(32), default="1.0.0")
    recommended_action = Column(String(32), nullable=False)
    decision_status = Column(String(32), nullable=False)
    risk_factors = Column(JSON, nullable=True)
    decision_reason = Column(Text, nullable=True)
    human_override = Column(Boolean, default=False)
    final_action = Column(String(32), nullable=False)
    operator_name = Column(String(64), default="System")

class MerchantSettingsModel(Base):
    __tablename__ = "merchant_settings"

    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(String(64), unique=True, index=True, default="DEFAULT")
    low_threshold = Column(Integer, default=30)
    medium_threshold = Column(Integer, default=70)
    verification_cost = Column(Float, default=25.0)
    manual_review_cost = Column(Float, default=65.0)
    false_positive_cost = Column(Float, default=220.0)
    average_loss_per_risky_order = Column(Float, default=2400.0)
    auto_approve_low_risk = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ModelVersionModel(Base):
    __tablename__ = "model_versions"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(String(32), unique=True, index=True, nullable=False)
    name = Column(String(64), nullable=False)
    algorithm = Column(String(64), nullable=False)
    precision = Column(Float, nullable=False)
    recall = Column(Float, nullable=False)
    f1_score = Column(Float, nullable=False)
    roc_auc = Column(Float, nullable=False)
    pr_auc = Column(Float, nullable=False)
    trained_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
