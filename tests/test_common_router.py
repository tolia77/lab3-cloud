from unittest.mock import patch


def test_healthcheck(client):
    """Test health check endpoint returns ok status."""
    response = client.get("/common/healthcheck")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["message"] == "Service is running"


def test_time(client):
    """Test time endpoint returns server time."""
    response = client.get("/common/time")
    assert response.status_code == 200
    assert "server_time" in response.json()


def test_unknown_route_returns_404(client):
    """Test that unknown routes return 404."""
    response = client.get("/common/not-existing-route")
    assert response.status_code == 404


def test_healthcheck_wrong_method(client):
    """Test that POST to healthcheck returns 405."""
    response = client.post("/common/healthcheck")
    assert response.status_code == 405


def test_time_internal_error(client):
    """Test time endpoint handles internal errors."""
    with patch("app.core.router.datetime.datetime") as mock_dt:
        mock_dt.now.side_effect = Exception("Internal error")
        response = client.get("/common/time")
        assert response.status_code == 500


def test_sentry_debug_returns_500(client):
    """Test sentry debug endpoint triggers error and returns 500."""
    response = client.get("/common/sentry-debug")
    assert response.status_code == 500


def test_time_response_format(client):
    """Test that time response has valid ISO format."""
    response = client.get("/common/time")
    assert response.status_code == 200
    data = response.json()
    assert "server_time" in data
    # Check that server_time is a valid ISO format string
    assert "T" in data["server_time"]


def test_root_endpoint(client):
    """Test root endpoint returns hello message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Hello World"


def test_hello_name_endpoint(client):
    """Test hello endpoint with name parameter."""
    response = client.get("/hello/TestUser")
    assert response.status_code == 200
    assert response.json()["message"] == "Hello TestUser"

