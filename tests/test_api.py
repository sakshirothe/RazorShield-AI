import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["model_loaded"] is True
    assert data["evaluation_available"] is True

def test_model_metrics_endpoint(client):
    response = client.get("/api/model/metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert "evaluation" in data
    eval_metrics = data["evaluation"]["metrics_summary"]
    assert "precision" in eval_metrics
    assert "recall" in eval_metrics
    assert "f1_score" in eval_metrics
    assert "roc_auc" in eval_metrics
    assert eval_metrics["roc_auc"] > 0.80

def test_dashboard_endpoint(client):
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "overview" in data
    assert data["overview"]["total_transactions"] >= 5
    assert "risk_distribution" in data
    assert len(data["category_breakdown"]) > 0

def test_analyze_low_risk_transaction(client):
    payload = {
        "order_value": 1200.0,
        "payment_method": "UPI",
        "product_category": "Fashion & Apparel",
        "quantity": 1,
        "account_age_days": 500,
        "previous_orders": 30,
        "previous_returns": 0,
        "previous_refunds": 0,
        "previous_rto_count": 0,
        "address_change_count": 0,
        "device_account_count": 1,
        "shipping_distance_km": 100.0,
        "pincode_risk_score": 0.15
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["decision"]["risk_level"] == "LOW"
    assert data["decision"]["recommended_action"] == "APPROVE"
    assert data["decision"]["risk_score"] <= 35
    assert len(data["top_protective_factors"]) > 0
    assert "LOW RISK" in data["ai_risk_assessment"]

def test_analyze_high_risk_transaction(client):
    payload = {
        "order_value": 7500.0,
        "payment_method": "COD",
        "product_category": "Electronics",
        "quantity": 2,
        "account_age_days": 3,
        "previous_orders": 4,
        "previous_returns": 3,
        "previous_refunds": 3,
        "previous_rto_count": 3,
        "orders_last_7_days": 4,
        "address_change_count": 3,
        "device_account_count": 4,
        "shipping_distance_km": 1800.0,
        "pincode_risk_score": 0.85
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["decision"]["risk_level"] in ["MEDIUM", "HIGH"]
    assert data["decision"]["recommended_action"] in ["MANUAL_REVIEW", "ADDITIONAL_VERIFICATION"]
    assert data["decision"]["estimated_loss"] > 0
    assert data["decision"]["expected_benefit"] > 0
    assert len(data["top_risk_factors"]) > 0

def test_simulate_endpoint(client):
    sim_payload = {
        "order_value": 5000.0,
        "payment_method": "COD",
        "product_category": "Electronics",
        "account_age_days": 5,
        "previous_orders": 2,
        "previous_returns": 2,
        "previous_rto_count": 1,
        "address_change_count": 2,
        "device_account_count": 3,
        "pincode_risk_score": 0.70
    }
    response = client.post("/api/simulate", json=sim_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["simulation_flag"] is True
    assert "decision" in data
    assert "top_risk_factors" in data

def test_review_queue_and_human_override(client):
    reviews_res = client.get("/api/reviews?limit=5")
    assert reviews_res.status_code == 200
    reviews = reviews_res.json()["items"]
    assert len(reviews) > 0

    first_review = reviews[0]
    review_id = first_review["id"]

    override_payload = {
        "action": "APPROVED",
        "reason": "Verified via WhatsApp confirmation call with customer",
        "operator_name": "Senior Risk Specialist"
    }
    decision_res = client.post(f"/api/reviews/{review_id}/decision", json=override_payload)
    assert decision_res.status_code == 200
    decision_data = decision_res.json()
    assert decision_data["new_status"] == "APPROVED"
    assert decision_data["audit_logged"] is True

    audit_res = client.get("/api/audit?limit=5")
    assert audit_res.status_code == 200
    audit_items = audit_res.json()["items"]
    assert any(
        item["transaction_id"] == first_review["transaction_id"] and "HUMAN_APPROVED" in item["decision_status"]
        for item in audit_items
    )
