# test_api.py
from fastapi.testclient import TestClient
from api_transform import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_transform_default_threshold():
    r = client.post("/transform", json={"name": "a", "score": 41})
    assert r.status_code == 200
    assert r.json()["passed"] is True


def test_transform_custom_threshold():
    r = client.post("/transform?threshold=50", json={"name": "a", "score": 41})
    assert r.status_code == 200
    assert r.json()["passed"] is False


def test_name_too_long():
    long_name = "a" * 60
    r = client.post("/transform", json={"name": long_name, "score": 90})
    assert r.status_code == 400
