from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

response = client.post("/register", data={
    "nome": "Test",
    "cpf": "123456",
    "email": "test4@test.com",
    "senha": "123"
})

print("Status code:", response.status_code)
print("Response:", response.text)
