from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend import schemas, crud, database
from backend.routers.auth import get_current_user

router = APIRouter(prefix="/transacoes", tags=["transacoes"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.TransacaoResponse)
def criar_transacao(transacao: schemas.TransacaoCreate,
                    db: Session = Depends(get_db),
                    usuario=Depends(get_current_user)):
    return crud.create_transacao(db, transacao, usuario.id)

@router.get("/", response_model=List[schemas.TransacaoResponse])
def listar_transacoes(db: Session = Depends(get_db),
                      usuario=Depends(get_current_user)):
    return crud.get_transacoes_by_usuario(db, usuario.id)
