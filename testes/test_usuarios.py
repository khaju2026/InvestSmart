def test_criar_usuario(client):
    response = client.post("/usuarios/", json={
        "nome": "Carlos Silva",
        "email": "carlos@email.com",
        "senha": "123456",
        "cpf": "12345678900"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "carlos@email.com"
    assert "id" in data
