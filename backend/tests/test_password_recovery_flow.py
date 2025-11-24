def test_phone_recovery_verify_reset(app_client):
    payload = {
        "phone": "15500000000",
        "idType": "身份证",
        "idNumber": "11010519491231002X"
    }
    resp = app_client.post('/api/auth/password/recovery/phone', json=payload)
    assert resp.status_code == 200
    data = resp.json()['data']
    token = data['token']
    assert token

    verify_payload = {"token": token, "verificationCode": "123456", "type": "phone"}
    verify_resp = app_client.post('/api/auth/password/recovery/verify', json=verify_payload)
    assert verify_resp.status_code == 200
    assert verify_resp.json()['code'] == 200

    reset_payload = {"token": token, "newPassword": "Abc12345", "confirmPassword": "Abc12345"}
    reset_resp = app_client.post('/api/auth/password/recovery/reset', json=reset_payload)
    assert reset_resp.status_code == 200
    assert reset_resp.json()['code'] == 200

