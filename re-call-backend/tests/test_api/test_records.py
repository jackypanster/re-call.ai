from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_records_ping():
    resp = client.get("/api/v1/records/ping")
    assert resp.status_code == 200
    assert resp.json() == {"msg": "records ok"} 