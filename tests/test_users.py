from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def make_user_payload():
    # Делаем каждый раз новый логин, чтобы уникальный constraint не срабатывал
    unique = uuid4()
    return {
        "login": f"test_{unique}@example.com",
        "password": "secret123",
        "project_id": str(uuid4()),
        "env": "prod",
        "domain": "regular",
    }


def test_create_user():
    payload = make_user_payload()
    response = client.post("/api/v1/users/", json=payload)
    print("RESPONSE STATUS:", response.status_code)
    print("RESPONSE JSON:", response.json())
    assert response.status_code == 201
    data = response.json()
    assert data["login"] == payload["login"]
    assert "id" in data
    assert data["locktime"] is None


def test_get_users():
    payload = make_user_payload()
    client.post("/api/v1/users/", json=payload)

    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_acquire_and_release_lock():
    payload = make_user_payload()
    created = client.post("/api/v1/users/", json=payload).json()
    user_id = created["id"]

    # acquire
    r1 = client.post(f"/api/v1/users/{user_id}/acquire_lock")
    assert r1.status_code == 200
    body = r1.json()
    assert body["locked"] is True
    assert body["locktime"] is not None

    # повторный acquire -> 409
    r2 = client.post(f"/api/v1/users/{user_id}/acquire_lock")
    assert r2.status_code == 409

    # release
    r3 = client.post(f"/api/v1/users/{user_id}/release_lock")
    assert r3.status_code == 200
    body2 = r3.json()
    assert body2["locked"] is False
    assert body2["locktime"] is None
