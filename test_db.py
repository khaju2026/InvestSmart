from backend.database import SessionLocal, engine
from backend import models, schemas
from backend.crud import create_usuario
import traceback

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    novo = schemas.UsuarioCreate(nome="Test", cpf="123", email="test@test.com", senha="123")
    create_usuario(db, novo)
    print("Sucesso!")
except Exception as e:
    print("Erro:")
    traceback.print_exc()
finally:
    db.close()
