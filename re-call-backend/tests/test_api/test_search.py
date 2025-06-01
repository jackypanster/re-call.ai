from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_ping():
    resp = client.get("/api/v1/search/ping")
    assert resp.status_code == 200
    assert resp.json() == {"msg": "search ok"} 