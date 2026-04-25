@app.get("/me/investimentos", response_model=list[schemas.Investimento])
def listar_meus_investimentos(
    usuario: models.Usuario = Depends(get_usuario_atual),
    db: Session = Depends(get_db)
):
    return db.query(models.Investimento).filter(models.Investimento.usuario_id == usuario.id).all()
