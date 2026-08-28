import pytest
from fastapi.testclient import TestClient

import app.db.factory as factory
from app.config import settings
from app.main import app


@pytest.fixture()
def client(monkeypatch):
    # Force in-memory storage for tests regardless of a configured Supabase
    # URL in the environment — tests must never write to a real project.
    monkeypatch.setattr(settings, "supabase_url", None)
    factory._repository_instance = None
    with TestClient(app) as test_client:
        yield test_client
    factory._repository_instance = None


def test_create_case_end_to_end_flow(client: TestClient):
    citizens = client.get("/api/citizens").json()
    ravi = next(c for c in citizens if c["persona_key"] == "ravi_kumar")

    create_resp = client.post(
        "/api/cases",
        json={
            "citizen_id": ravi["id"],
            "raw_text": "The streetlight outside my house hasn't worked for two weeks.",
            "location_text": "Narapally, Hyderabad",
        },
    )
    assert create_resp.status_code == 200
    body = create_resp.json()
    assert body["redirected"] is False
    case_number = body["case"]["case_number"]
    assert body["case"]["understanding"]["category"] == "streetlight"

    detail_resp = client.get(f"/api/cases/{case_number}")
    assert detail_resp.status_code == 200
    assert detail_resp.json()["status"] == "in_progress"


def test_full_streetlight_hero_resolution_loop(client: TestClient):
    case_number = "CIV-20481"

    detail = client.get(f"/api/cases/{case_number}").json()
    assert detail["sla"]["is_overdue"] is True
    assert detail["can_escalate"] is True

    escalate_resp = client.post(f"/api/cases/{case_number}/escalate", json={"citizen_id": "ravi"})
    assert escalate_resp.status_code == 200
    assert len(escalate_resp.json()["escalations"]) == 1

    again_resp = client.post(f"/api/cases/{case_number}/escalate", json={"citizen_id": "ravi"})
    assert again_resp.status_code == 400

    resolved_resp = client.post(f"/api/admin/cases/{case_number}/mark-resolved")
    assert resolved_resp.status_code == 200
    resolved_body = resolved_resp.json()
    assert resolved_body["status"] == "resolved_pending_verification"
    assert resolved_body["awaiting_citizen_verification"] is True
    verification_stages = [t for t in resolved_body["timeline"] if t["stage_name"] == "Citizen Verification"]
    assert len(verification_stages) == 1

    verify_no_resp = client.post(
        f"/api/cases/{case_number}/verify",
        json={"citizen_id": "ravi", "is_actually_fixed": False, "explanation_text": "Still dark at night."},
    )
    assert verify_no_resp.status_code == 200
    reopened_body = verify_no_resp.json()
    assert reopened_body["status"] == "reopened"
    assert "sent it back" in reopened_body["explanation"]["whats_happening"]

    resolved_again_resp = client.post(f"/api/admin/cases/{case_number}/mark-resolved")
    assert resolved_again_resp.status_code == 200
    verification_stages_again = [t for t in resolved_again_resp.json()["timeline"] if t["stage_name"] == "Citizen Verification"]
    assert len(verification_stages_again) == 1

    verify_yes_resp = client.post(
        f"/api/cases/{case_number}/verify",
        json={"citizen_id": "ravi", "is_actually_fixed": True, "explanation_text": None},
    )
    assert verify_yes_resp.status_code == 200
    closed_body = verify_yes_resp.json()
    assert closed_body["status"] == "closed"
    assert closed_body["awaiting_citizen_verification"] is False
    assert "now closed" in closed_body["explanation"]["whats_happening"]


def test_domain_switch_pf_scenario(client: TestClient):
    detail = client.get("/api/cases/PF-28491").json()
    assert detail["authority"]["authority_type"] == "epfo"
    assert detail["explanation"]["who_needs_to_act"] == "Your employer"
    assert len(detail["escalations"]) == 1


def test_safety_screen_redirects_emergency_text(client: TestClient):
    citizens = client.get("/api/citizens").json()
    citizen_id = citizens[0]["id"]
    resp = client.post(
        "/api/cases",
        json={"citizen_id": citizen_id, "raw_text": "There is a fire spreading near my house right now, someone is dying"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["redirected"] is True
    assert "emergency" in body["redirect"]["reason"]
