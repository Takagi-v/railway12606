import pytest


def test_apply_membership_requires_auth(client):
    payload = {
        "name": "张三",
        "idType": "居民身份证",
        "idNumber": "123456789012345678",
        "birthDate": "2010-05-01",
        "phone": "13800138000",
        "email": "user@example.com"
    }
    r = client.post("/api/v1/members", json=payload)
    assert r.status_code == 401


def test_get_members_me_ok(client):
    headers = {"Authorization": "Bearer dummy"}
    r = client.get("/api/v1/members/me", headers=headers)
    assert r.status_code == 200


def test_points_balance_ok(client):
    headers = {"Authorization": "Bearer dummy"}
    r = client.get("/api/v1/points", headers=headers)
    assert r.status_code == 200


def test_points_supplement_accepts(client):
    headers = {"Authorization": "Bearer dummy", "Idempotency-Key": "k1"}
    payload = {
        "ticketNo": "E1234567890",
        "trainNo": "G1234",
        "departDate": "2025-10-01",
        "passengerIdType": "居民身份证",
        "passengerIdNumber": "123456789012345678"
    }
    r = client.post("/api/v1/points/supplements", headers=headers, json=payload)
    assert r.status_code == 202


def test_beneficiaries_add_created(client):
    headers = {"Authorization": "Bearer dummy"}
    payload = {"name": "李四", "idType": "居民身份证", "idNumber": "123456789012345679"}
    r = client.post("/api/v1/beneficiaries", headers=headers, json=payload)
    assert r.status_code == 201


def test_redemptions_options_ok(client):
    headers = {"Authorization": "Bearer dummy"}
    params = {"from": "SHH", "to": "BJP", "date": "2025-11-20"}
    r = client.get("/api/v1/redemptions/options", headers=headers, params=params)
    assert r.status_code == 200


def test_redemptions_ticket_created(client):
    headers = {"Authorization": "Bearer dummy", "Idempotency-Key": "k2"}
    payload = {
        "passengerUse": "self",
        "from": "SHH",
        "to": "BJP",
        "date": "2025-11-20",
        "trainNo": "G1234",
        "class": "second",
        "seats": 1
    }
    r = client.post("/api/v1/redemptions/tickets", headers=headers, json=payload)
    assert r.status_code == 201