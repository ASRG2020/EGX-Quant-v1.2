from fastapi.testclient import TestClient
from app.api.main import app
client=TestClient(app)

def test_health():
    r=client.get("/health"); assert r.status_code==200; assert r.json()["status"]=="healthy"

def test_signal():
    r=client.get("/api/v1/signal/COMI"); assert r.status_code==200; assert r.json()["action"] in {"BUY","HOLD","SELL"}
