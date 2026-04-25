def test_criar_transacao(client):
    login = client.post("/login/", data={
        "username": "carlos@email.com",
        "password": "123456"
    })
    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/transacoes/", json={
        "tipo": "compra",
        "quantidade": 100,
        "preco": 25.50,
        "data": "2026-03-31",
        "investimento_id": 1,
        "usuario_id": 1
    }, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["tipo"] == "compra"
    assert data["quantidade"] == 100
    assert data["preco"] == 25.50
