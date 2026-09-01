import os

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "unit-test-secret-key-not-for-prod")
os.environ.setdefault("ENV", "test")

from fastapi.testclient import TestClient

from app.main import app
from app.db.session import Base, engine

Base.metadata.create_all(bind=engine)
client = TestClient(app)


def test_register_and_login_and_me():
    email = "user@example.com"
    password = "GoodPass1234"
    r = client.post("/api/v1/auth/register", json={"email": email, "password": password, "full_name": "U"})
    assert r.status_code == 201, r.text
    r2 = client.post("/api/v1/auth/register", json={"email": email, "password": password})
    assert r2.status_code == 409
    bad = client.post("/api/v1/auth/login", json={"username": email, "password": "wrong-pass-1"})
    assert bad.status_code == 401
    ok = client.post("/api/v1/auth/login", json={"username": email, "password": password})
    assert ok.status_code == 200
    token = ok.json()["access_token"]
    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == email


def test_weak_password_rejected():
    r = client.post("/api/v1/auth/register", json={"email": "weak@example.com", "password": "admin123"})
    assert r.status_code == 422


def test_invalid_jwt_rejected():
    r = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer not-a-jwt"})
    assert r.status_code == 401


def test_unauthenticated_files():
    r = client.get("/api/v1/files/sample")
    assert r.status_code in (401, 403)


def test_health_live():
    r = client.get("/health/live")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
