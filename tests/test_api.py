from fastapi import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    
def test_health_detailed():
    response = client.get("/api/v1/health/detailed")
    assert response.status_code == 200
    assert "components" in response.json()
    
def test_query_invalid_domain():
    response = client.post("/api/v1/query", json={
        "question": "test question",
        "domain": "invalid_domain"
    })
    assert response.status_code == 400