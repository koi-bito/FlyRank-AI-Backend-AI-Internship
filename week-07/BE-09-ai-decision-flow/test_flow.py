import pytest
from fastapi.testclient import TestClient
from main import app
from sample_flows import SUPPORT_TRIAGE_FLOW, SECURITY_GATE_FLOW

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_sample_flows():
    res = client.get("/api/sample-flows")
    assert res.status_code == 200
    flows = res.json()
    assert "support-ticket-triage" in flows
    assert "pr-security-gate" in flows

def test_support_triage_billing_branch():
    payload = {
        "graph": SUPPORT_TRIAGE_FLOW.model_dump(),
        "input_context": "I was billed twice on my Mastercard for subscription invoice #8812."
    }
    res = client.post("/api/run", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "COMPLETED"
    assert "Priority Billing" in data["final_outcome"]
    
    # Verify trace steps
    dec_step = next(s for s in data["trace"] if s["node_id"] == "node-billing")
    assert dec_step["decision"] == "YES"

def test_support_triage_urgent_oncall_branch():
    payload = {
        "graph": SUPPORT_TRIAGE_FLOW.model_dump(),
        "input_context": "CRITICAL EMERGENCY: Production cluster is down and returning 500 crashes!"
    }
    res = client.post("/api/run", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "COMPLETED"
    assert "On-Call Engineer" in data["final_outcome"]

    # Verify trace steps
    billing_step = next(s for s in data["trace"] if s["node_id"] == "node-billing")
    assert billing_step["decision"] == "NO"
    urgent_step = next(s for s in data["trace"] if s["node_id"] == "node-urgent")
    assert urgent_step["decision"] == "YES"

def test_support_triage_standard_support_branch():
    payload = {
        "graph": SUPPORT_TRIAGE_FLOW.model_dump(),
        "input_context": "Could you please explain how to change my username in user preferences?"
    }
    res = client.post("/api/run", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "COMPLETED"
    assert "Standard Support Desk" in data["final_outcome"]

def test_run_history_endpoint():
    payload = {
        "graph": SUPPORT_TRIAGE_FLOW.model_dump(),
        "input_context": "Testing run history retrieval"
    }
    res = client.post("/api/run", json=payload)
    run_id = res.json()["run_id"]

    hist_res = client.get(f"/api/runs/{run_id}")
    assert hist_res.status_code == 200
    assert hist_res.json()["run_id"] == run_id

def test_empty_graph_validation():
    payload = {
        "graph": {"id": "invalid", "name": "bad", "nodes": [], "edges": []},
        "input_context": "dummy"
    }
    res = client.post("/api/run", json=payload)
    assert res.status_code == 400

if __name__ == "__main__":
    test_health()
    test_sample_flows()
    test_support_triage_billing_branch()
    test_support_triage_urgent_oncall_branch()
    test_support_triage_standard_support_branch()
    test_run_history_endpoint()
    test_empty_graph_validation()
    print("All BE-09 AI Decision Flow Tests Passed Successfully!")
