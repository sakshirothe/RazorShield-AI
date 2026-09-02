import os
import joblib
from typing import Dict, Any

from backend.app.core.config import settings
from backend.app.services.decision_engine import evaluate_cost_sensitive_decision
from backend.app.services.agent_service import AIRiskManagerAgent
from ml.features import engineer_features
from ml.explain import explain_prediction

class RiskPredictor:
    _instance = None
    _model = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.model_path = settings.MODEL_PATH
        if os.path.exists(self.model_path):
            self._model = joblib.load(self.model_path)
        else:
            self._model = None

    def predict_transaction(
        self,
        transaction_data: Dict[str, Any],
        merchant_settings: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        if self._model is None:
            if os.path.exists(self.model_path):
                self._model = joblib.load(self.model_path)
            else:
                raise RuntimeError("ML Model weights file is missing. Please train model first.")

        X = engineer_features(transaction_data)
        risk_probability = float(self._model.predict_proba(X)[:, 1][0])

        explanation = explain_prediction(self._model, transaction_data, top_n=5)
        top_risk_factors = explanation["top_risk_factors"]
        top_protective_factors = explanation["top_protective_factors"]

        order_val = float(transaction_data.get("order_value", 1000.0))
        decision = evaluate_cost_sensitive_decision(
            risk_probability=risk_probability,
            order_value=order_val,
            settings=merchant_settings
        )

        ai_assessment = AIRiskManagerAgent.generate_assessment(
            transaction_dict=transaction_data,
            decision=decision,
            top_risk_factors=top_risk_factors,
            top_protective_factors=top_protective_factors
        )

        return {
            "decision": decision,
            "top_risk_factors": top_risk_factors,
            "top_protective_factors": top_protective_factors,
            "ai_risk_assessment": ai_assessment,
            "metadata": {
                "model_version": settings.APP_VERSION,
                "base_value": explanation["base_value"],
                "disclaimer": explanation["disclaimer"]
            }
        }

risk_predictor = RiskPredictor.get_instance()
