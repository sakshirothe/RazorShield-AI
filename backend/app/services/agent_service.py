from typing import Dict, List, Any

class AIRiskManagerAgent:
    @staticmethod
    def generate_assessment(
        transaction_dict: Dict[str, Any],
        decision: Dict[str, Any],
        top_risk_factors: List[Dict[str, Any]],
        top_protective_factors: List[Dict[str, Any]]
    ) -> str:
        risk_score = decision["risk_score"]
        risk_level = decision["risk_level"]
        action = decision["recommended_action"]
        potential_loss = decision["estimated_loss"]
        cost = decision["intervention_cost"]
        benefit = decision["expected_benefit"]

        order_val = transaction_dict.get("order_value", 0.0)
        pay_method = transaction_dict.get("payment_method", "N/A")
        cat = transaction_dict.get("product_category", "Goods")

        if top_risk_factors:
            primary_drivers = ", ".join([f["feature_name"] for f in top_risk_factors[:3]])
        else:
            primary_drivers = "No significant risk flags detected"

        if top_protective_factors:
            protective_drivers = ", ".join([f["feature_name"] for f in top_protective_factors[:2]])
        else:
            protective_drivers = "standard baseline parameters"

        if risk_level == "HIGH":
            narrative = (
                f"Order of ₹{order_val:,.2f} ({pay_method}, {cat}) is classified as HIGH RISK "
                f"(Score: {risk_score}/100). The primary risk drivers are {primary_drivers}. "
                f"Estimated RTO/abuse loss is ₹{potential_loss:,.2f}. Based on cost optimization, "
                f"allocating ₹{cost:,.2f} for {action.replace('_', ' ').lower()} yields an expected net benefit "
                f"of ₹{benefit:,.2f}. Human operator verification is strongly recommended."
            )
        elif risk_level == "MEDIUM":
            narrative = (
                f"Order of ₹{order_val:,.2f} presents MODERATE RISK (Score: {risk_score}/100), "
                f"moderated by {protective_drivers}, but elevated by {primary_drivers}. "
                f"Potential loss is estimated at ₹{potential_loss:,.2f}. Recommending {action.replace('_', ' ').lower()} "
                f"(cost: ₹{cost:,.2f}) to prevent doorstep delivery rejection before logistics dispatch."
            )
        else:
            narrative = (
                f"Order of ₹{order_val:,.2f} is classified as LOW RISK (Score: {risk_score}/100). "
                f"Customer profile exhibits favorable signals including {protective_drivers}. "
                f"Immediate approval is recommended to ensure zero customer friction."
            )

        return narrative

    @staticmethod
    def execute_bounded_action(
        action_name: str,
        transaction_id: str,
        decision: Dict[str, Any],
        operator_notes: str = ""
    ) -> Dict[str, Any]:
        allowed_actions = {
            "APPROVE_ORDER",
            "REQUEST_VERIFICATION",
            "ROUTE_TO_MANUAL_REVIEW",
            "OVERRIDE_TO_APPROVE",
            "OVERRIDE_TO_REJECT"
        }
        if action_name not in allowed_actions:
            raise ValueError(f"Action '{action_name}' is not an authorized bounded agent action.")

        return {
            "status": "EXECUTED",
            "action": action_name,
            "transaction_id": transaction_id,
            "risk_score": decision.get("risk_score"),
            "risk_level": decision.get("risk_level"),
            "audit_trail_recorded": True,
            "notes": operator_notes or "Executed by AI Risk Manager Agent under policy bounds"
        }
