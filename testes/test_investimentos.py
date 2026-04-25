def test_criar_investimento(client):
    # Primeiro, login para pegar token
    login = client.post("/login/", data={
        "username": "carlos@email.com",
        "password": "123456"
    })
    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/investimentos/", json={
        "nome": "Ações Petrobras",
        "valor": 10000.0,
        "usuario_id": 1
    }, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Ações Petrobras"
    assert data["valor"] == 10000.0
