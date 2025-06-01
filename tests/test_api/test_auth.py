from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_auth_ping():
    resp = client.get("/api/v1/auth/ping")
    assert resp.status_code == 200
    assert resp.json() == {"msg": "auth ok"} 