import requests

def test_health_endpoint_returns_healthy(base_url):
    response = requests.get(f"{base_url}/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_api_auth_register(base_url, user_info):
    response = requests.post(f"{base_url}/api/auth/register", json=user_info)
    assert response.status_code == 201
    data = response.json()
    print(data)
    assert data["user"]["username"] == user_info["username"]


def test_login_returns_jwt_token(base_url,user_account):
    response = requests.post(f"{base_url}/api/auth/login", json=user_account)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_create_event_success(base_url, event_data, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = requests.post(
        f"{base_url}/api/events",
        json=event_data,
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == event_data["title"]

def test_rsvp_to_public_event_succeeds_without_auth(base_url, public_event_id):
    response = requests.get(f"{base_url}/api/rsvps/event/{public_event_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["event"]["id"] == public_event_id


def test_register_duplicate_username_fails(base_url, user_account):
    """Error: Registration with an existing username should return 400."""
    response = requests.post(f"{base_url}/api/auth/register", json=user_account)
    assert response.status_code == 400


def test_create_event_without_auth_fails(base_url, event_data):
    """Error: Creating an event without a token should return 401."""
    response = requests.post(f"{base_url}/api/events", json=event_data)
    assert response.status_code == 401


def test_rsvp_to_private_event_without_auth_fails(base_url, auth_token,
                                                  event_data):
    """Error: RSVP to a private event without auth should return 401."""
    private_data = event_data.copy()
    private_data["is_public"] = False

    headers = {"Authorization": f"Bearer {auth_token}"}
    event_res = requests.post(f"{base_url}/api/events", json=private_data,
                              headers=headers)
    event_id = event_res.json()["id"]

    response = requests.post(f"{base_url}/api/rsvps/event/{event_id}", json={})
    assert response.status_code in (401, 403)


