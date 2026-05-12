import requests
import time
import subprocess

# Inicia o servidor em background
proc = subprocess.Popen(["uvicorn", "main:app", "--port", "8005"])
time.sleep(3)

try:
    # Faz um POST pro /register
    data = {
        "nome": "Test User",
        "cpf": "12345678900",
        "email": "test@test.com",
        "senha": "password"
    }
    r = requests.post("http://127.0.0.1:8005/register", data=data)
    print("Status:", r.status_code)
    if r.status_code == 500:
        print("Body:", r.text)
except Exception as e:
    print("Error:", e)
finally:
    proc.terminate()
