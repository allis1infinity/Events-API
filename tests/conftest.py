import pytest
import requests
import uuid

@pytest.fixture
def base_url():
    return "http://localhost:5000"

@pytest.fixture
def user_info():
    """Generate a random username and password."""
    unique_id = uuid.uuid4()
    unique_username = f"user_{unique_id}"
    return {
        "username": unique_username,
        "password": "PASSWORD_123"
    }

@pytest.fixture
def user_account(base_url, user_info):
    """Create a new user account and return its login details."""
    requests.post(f"{base_url}/api/auth/register", json=user_info)
    return user_info


@pytest.fixture
def auth_token(base_url, user_account):
    """Login to the application and return the JWT token."""
    response = requests.post(f"{base_url}/api/auth/login", json=user_account)
    return response.json()["access_token"]


@pytest.fixture
def event_data():
    """Return a dictionary with  event details."""
    return {
        "title": "New Easy Event",
        "date": "2026-10-10T10:00:00",
        "is_public": True
    }

@pytest.fixture
def public_event_id(base_url, auth_token, event_data):
    """Create a public event and return its ID."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{base_url}/api/events", json=event_data, headers=headers)
    return response.json()["id"]


