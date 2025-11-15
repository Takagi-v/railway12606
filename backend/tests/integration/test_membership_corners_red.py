import pytest


def test_membership_apply_underage_422(client):
    headers = {"Authorization": "Bearer dummy"}
    payload = {
        "name": "小明",
        "idType": "居民身份证",
        "idNumber": "123456789012345670",
        "birthDate": "2020-01-01",
        "phone": "13800138001",
        "email": "child@example.com"
    }
    r = client.post("/api/v1/members", headers=headers, json=payload)
    assert r.status_code == 422


def test_membership_apply_duplicate_409(client):
    headers = {"Authorization": "Bearer dummy"}
    payload = {
        "name": "张三",
        "idType": "居民身份证",
        "idNumber": "123456789012345678",
        "birthDate": "1990-05-01",
        "phone": "13800138000",
        "email": "user@example.com"
    }
    client.post("/api/v1/members", headers=headers, json=payload)
    r = client.post("/api/v1/members", headers=headers, json=payload)
    assert r.status_code == 409


def test_membership_me_requires_auth_401(client):
    r = client.get("/api/v1/members/me")
    assert r.status_code == 401


def test_points_supplement_missing_idempotency_400(client):
    headers = {"Authorization": "Bearer dummy"}
    payload = {
        "ticketNo": "E1234567890",
        "trainNo": "G1234",
        "departDate": "2025-10-01",
        "passengerIdType": "居民身份证",
        "passengerIdNumber": "123456789012345678"
    }
    r = client.post("/api/v1/points/supplements", headers=headers, json=payload)
    assert r.status_code == 400


def test_redemptions_ticket_missing_idempotency_400(client):
    headers = {"Authorization": "Bearer dummy"}
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
    assert r.status_code == 400


def test_redemptions_options_missing_params_400(client):
    headers = {"Authorization": "Bearer dummy"}
    r = client.get("/api/v1/redemptions/options", headers=headers)
    assert r.status_code == 400


def test_beneficiaries_add_missing_id_number_400(client):
    headers = {"Authorization": "Bearer dummy"}
    payload = {"name": "李四", "idType": "居民身份证"}
    r = client.post("/api/v1/beneficiaries", headers=headers, json=payload)
    assert r.status_code == 400


def test_points_exclusions_ok_200(client):
    headers = {"Authorization": "Bearer dummy"}
    r = client.get("/api/v1/points/exclusions", headers=headers)
    assert r.status_code == 200


def test_privileges_list_ok_200(client):
    headers = {"Authorization": "Bearer dummy"}
    r = client.get("/api/v1/privileges", headers=headers)
    assert r.status_code == 200


def test_stations_member_service_ok_200(client):
    r = client.get("/api/v1/stations/member-service")
    assert r.status_code == 200


def test_points_supplement_idempotency_second_200(client):
    headers = {"Authorization": "Bearer dummy", "Idempotency-Key": "same-key"}
    payload = {
        "ticketNo": "E1234567890",
        "trainNo": "G1234",
        "departDate": "2025-10-01",
        "passengerIdType": "居民身份证",
        "passengerIdNumber": "123456789012345678"
    }
    first = client.post("/api/v1/points/supplements", headers=headers, json=payload)
    second = client.post("/api/v1/points/supplements", headers=headers, json=payload)
    assert first.status_code == 202
    assert second.status_code == 200