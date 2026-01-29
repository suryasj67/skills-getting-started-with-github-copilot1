import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball" in data

def test_signup_and_unregister():
    test_email = "testuser@mergington.edu"
    activity = "Basketball"
    # Signup
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 200
    # Check participant added
    response = client.get("/activities")
    participants = response.json()[activity]["participants"]
    assert test_email in participants
    # Unregister
    response = client.post(f"/activities/{activity}/unregister", json={"email": test_email})
    assert response.status_code == 200
    # Check participant removed
    response = client.get("/activities")
    participants = response.json()[activity]["participants"]
    assert test_email not in participants
