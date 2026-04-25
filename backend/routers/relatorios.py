from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend import schemas, crud, database
from backend.routers.auth import get_current_user

router = APIRouter(prefix="/relatorios", tags=["relatorios"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/carteira", response_model=schemas.RelatorioCarteira)
def relatorio_carteira(db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    return crud.gerar_relatorio_carteira(db, usuario.id)
