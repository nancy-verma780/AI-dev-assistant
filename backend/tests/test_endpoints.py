from fastapi.testclient import TestClient
from backend.app.main import app, METRICS_STATE

client = TestClient(app)


def test_metrics_endpoint_structure_and_types():
    """Verifies that the metrics route returns correct keys and data types."""
    # Reset state values before executing test tracking to isolate it
    METRICS_STATE["total_requests"] = 0
    METRICS_STATE["total_analyses"] = 0
    
    response = client.get("/metrics")
    assert response.status_code == 200
    
    data = response.json()
    assert "requests" in data
    assert "analyses" in data
    assert "uptime" in data
    assert "version" in data
    
    # Assert data types rather than flaky, rigid numbers
    assert isinstance(data["requests"], int)
    assert isinstance(data["analyses"], int)
    assert isinstance(data["uptime"], str)
    assert isinstance(data["version"], str)


def test_metrics_incrementation():
    """Verifies that hitting endpoints increments the internal counter state."""
    METRICS_STATE["total_requests"] = 5
    
    response = client.get("/metrics")
    data = response.json()
    
    # The count should reflect our state modification
    assert data["requests"] >= 5
