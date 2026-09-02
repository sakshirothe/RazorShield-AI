from typing import Dict, Any

def evaluate_cost_sensitive_decision(
    risk_probability: float,
    order_value: float,
    settings: Dict[str, Any] = None
) -> Dict[str, Any]:
    if settings is None:
        settings = {}

    low_threshold = settings.get("low_threshold", 30)
    medium_threshold = settings.get("medium_threshold", 70)
    verification_cost = settings.get("verification_cost", 25.0)
    manual_review_cost = settings.get("manual_review_cost", 65.0)
    false_pos_cost = settings.get("false_positive_cost", 220.0)

    risk_score = int(round(risk_probability * 100))

    if risk_score <= low_threshold:
        risk_level = "LOW"
    elif risk_score <= medium_threshold:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    estimated_potential_loss = round(350.0 + (0.15 * order_value), 2)
    expected_avoided_loss = round(risk_probability * estimated_potential_loss, 2)

    expected_verification_benefit = round((expected_avoided_loss * 0.85) - verification_cost, 2)
    potential_fp_friction = (1.0 - risk_probability) * 0.05 * false_pos_cost
    expected_review_benefit = round((expected_avoided_loss * 0.95) - (manual_review_cost + potential_fp_friction), 2)

    if risk_level == "HIGH":
        if expected_review_benefit > 0 and expected_review_benefit >= expected_verification_benefit:
            action = "MANUAL_REVIEW"
            chosen_cost = manual_review_cost
            chosen_benefit = expected_review_benefit
            reason = (
                f"High risk score ({risk_score}/100). Potential loss ₹{estimated_potential_loss:.2f} "
                f"justifies manual risk review (expected net savings ₹{chosen_benefit:.2f})."
            )
        elif expected_verification_benefit > 0:
            action = "ADDITIONAL_VERIFICATION"
            chosen_cost = verification_cost
            chosen_benefit = expected_verification_benefit
            reason = (
                f"High risk score ({risk_score}/100) with moderate order value. Automated verification "
                f"yields optimal return (net savings ₹{chosen_benefit:.2f})."
            )
        else:
            action = "APPROVE"
            chosen_cost = 0.0
            chosen_benefit = 0.0
            reason = "Intervention costs exceed expected avoided loss. Economically optimal to approve."
    elif risk_level == "MEDIUM":
        if expected_verification_benefit > 0:
            action = "ADDITIONAL_VERIFICATION"
            chosen_cost = verification_cost
            chosen_benefit = expected_verification_benefit
            reason = (
                f"Medium risk score ({risk_score}/100). Automated verification (OTP / address check) "
                f"is cost-effective (expected net benefit ₹{chosen_benefit:.2f})."
            )
        else:
            action = "APPROVE"
            chosen_cost = 0.0
            chosen_benefit = 0.0
            reason = "Medium risk, but low order value makes intervention uneconomical. Approved."
    else:
        action = "APPROVE"
        chosen_cost = 0.0
        chosen_benefit = 0.0
        reason = f"Low risk score ({risk_score}/100). Seamless checkout approved with zero friction."

    return {
        "risk_score": risk_score,
        "risk_probability": round(risk_probability, 4),
        "risk_level": risk_level,
        "recommended_action": action,
        "estimated_loss": estimated_potential_loss,
        "intervention_cost": chosen_cost,
        "expected_benefit": max(chosen_benefit, 0.0),
        "reason": reason
    }
