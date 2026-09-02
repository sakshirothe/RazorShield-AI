from backend.app.services.decision_engine import evaluate_cost_sensitive_decision

def test_low_risk_approval():
    result = evaluate_cost_sensitive_decision(
        risk_probability=0.08,
        order_value=1500.0
    )
    assert result["risk_level"] == "LOW"
    assert result["recommended_action"] == "APPROVE"
    assert result["intervention_cost"] == 0.0

def test_high_risk_manual_review():
    result = evaluate_cost_sensitive_decision(
        risk_probability=0.85,
        order_value=8000.0
    )
    assert result["risk_level"] == "HIGH"
    assert result["recommended_action"] == "MANUAL_REVIEW"
    assert result["expected_benefit"] > 0
    assert result["intervention_cost"] == 65.0

def test_medium_risk_additional_verification():
    result = evaluate_cost_sensitive_decision(
        risk_probability=0.45,
        order_value=3000.0
    )
    assert result["risk_level"] == "MEDIUM"
    assert result["recommended_action"] == "ADDITIONAL_VERIFICATION"
    assert result["intervention_cost"] == 25.0
    assert result["expected_benefit"] > 0

def test_configurable_threshold_overrides():
    custom_settings = {
        "low_threshold": 15,
        "medium_threshold": 40,
        "verification_cost": 20.0,
        "manual_review_cost": 50.0
    }
    result = evaluate_cost_sensitive_decision(
        risk_probability=0.25,
        order_value=4000.0,
        settings=custom_settings
    )
    assert result["risk_level"] == "MEDIUM"
    assert result["recommended_action"] == "ADDITIONAL_VERIFICATION"
