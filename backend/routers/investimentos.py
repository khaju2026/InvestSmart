from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend import schemas, crud, database
from backend.routers.auth import get_current_user

router = APIRouter(prefix="/investimentos", tags=["investimentos"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.InvestimentoResponse)
def criar_investimento(investimento: schemas.InvestimentoCreate,
                       db: Session = Depends(get_db),
                       usuario=Depends(get_current_user)):
    return crud.create_investimento(db, investimento, usuario.id)

@router.get("/", response_model=List[schemas.InvestimentoResponse])
def listar_investimentos(db: Session = Depends(get_db),
                         usuario=Depends(get_current_user)):
    return crud.get_investimentos_by_usuario(db, usuario.id)
