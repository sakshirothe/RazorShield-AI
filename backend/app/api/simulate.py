from fastapi import APIRouter
from backend.app.schemas.pydantic_schemas import SimulationInput
from backend.app.services.ml_predictor import risk_predictor

router = APIRouter(prefix="/api", tags=["Simulation"])

@router.post("/simulate")
def simulate_risk(payload: SimulationInput):
    sim_data = {
        "order_value": payload.order_value,
        "payment_method": payload.payment_method,
        "product_category": payload.product_category,
        "quantity": 1,
        "account_age_days": payload.account_age_days,
        "previous_orders": payload.previous_orders,
        "previous_returns": payload.previous_returns,
        "previous_refunds": payload.previous_returns,
        "previous_rto_count": payload.previous_rto_count,
        "days_since_last_order": 20,
        "orders_last_7_days": min(payload.previous_orders, 2),
        "orders_last_30_days": min(payload.previous_orders, 5),
        "address_change_count": payload.address_change_count,
        "device_account_count": payload.device_account_count,
        "shipping_distance_km": payload.shipping_distance_km,
        "pincode_risk_score": payload.pincode_risk_score,
        "delivery_attempts": 0,
        "payment_failure_count": 0,
        "previous_chargebacks": 0,
        "historical_customer_risk": round(
            (payload.previous_returns / max(payload.previous_orders, 1)) * 0.5 +
            (payload.device_account_count - 1) * 0.1,
            2
        )
    }

    result = risk_predictor.predict_transaction(sim_data)

    return {
        "simulation_flag": True,
        "disclaimer": "This is a model simulation, not a historical transaction.",
        "input_parameters": {
            "order_value": payload.order_value,
            "payment_method": payload.payment_method,
            "account_age_days": payload.account_age_days,
            "previous_returns": payload.previous_returns,
            "previous_orders": payload.previous_orders,
            "address_change_count": payload.address_change_count,
            "device_account_count": payload.device_account_count,
            "pincode_risk_score": payload.pincode_risk_score
        },
        "decision": result["decision"],
        "top_risk_factors": result["top_risk_factors"],
        "top_protective_factors": result["top_protective_factors"],
        "ai_risk_assessment": result["ai_risk_assessment"]
    }
