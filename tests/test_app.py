"""
Tests for the Mergington High School API
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from app import app, activities

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to original state before each test"""
    original = {
        name: {**data, "participants": list(data["participants"])}
        for name, data in activities.items()
    }
    yield
    activities.clear()
    activities.update(original)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for activity in data.values():
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity


def test_signup_for_activity():
    response = client.post(
        "/activities/Chess Club/signup?email=test@mergington.edu"
    )
    assert response.status_code == 200
    assert "test@mergington.edu" in response.json()["message"]


def test_signup_activity_not_found():
    response = client.post(
        "/activities/Unknown Activity/signup?email=test@mergington.edu"
    )
    assert response.status_code == 404


def test_signup_duplicate_registration():
    client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    response = client.post(
        "/activities/Chess Club/signup?email=test@mergington.edu"
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_unregister_from_activity():
    client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    response = client.delete(
        "/activities/Chess Club/signup?email=test@mergington.edu"
    )
    assert response.status_code == 200
    assert "test@mergington.edu" in response.json()["message"]


def test_unregister_activity_not_found():
    response = client.delete(
        "/activities/Unknown Activity/signup?email=test@mergington.edu"
    )
    assert response.status_code == 404


def test_unregister_student_not_registered():
    response = client.delete(
        "/activities/Chess Club/signup?email=notregistered@mergington.edu"
    )
    assert response.status_code == 404
