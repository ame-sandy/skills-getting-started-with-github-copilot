import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Ensure not already signed up
    client.delete(f"/activities/{activity}/participant?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Duplicate signup should fail
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400


def test_remove_participant():
    email = "removeme@mergington.edu"
    activity = "Art Club"
    # Sign up first
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.delete(f"/activities/{activity}/participant?email={email}")
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]
    # Removing again should fail
    response2 = client.delete(f"/activities/{activity}/participant?email={email}")
    assert response2.status_code == 404


def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404


def test_remove_invalid_activity():
    response = client.delete("/activities/Nonexistent/participant?email=test@mergington.edu")
    assert response.status_code == 404


def test_remove_invalid_participant():
    response = client.delete("/activities/Chess Club/participant?email=notfound@mergington.edu")
    assert response.status_code == 404
