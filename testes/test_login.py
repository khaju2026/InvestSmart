def test_login_usuario(client):
    response = client.post("/login/", data={
        "username": "carlos@email.com",
        "password": "123456"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
