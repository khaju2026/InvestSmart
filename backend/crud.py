from sqlalchemy.orm import Session
from backend import models, schemas
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# Usuários
def get_usuario_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def get_usuario_by_cpf(db: Session, cpf: str):
    return db.query(models.Usuario).filter(models.Usuario.cpf == cpf).first()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    senha_hash = hash_password(usuario.senha)
    novo_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=senha_hash,
        cpf=usuario.cpf
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

# Investimentos
def create_investimento(db: Session, investimento: schemas.InvestimentoCreate, usuario_id: int):
    novo = models.Investimento(
        nome=investimento.nome,
        valor=investimento.valor,
        usuario_id=usuario_id
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

def get_investimentos_by_usuario(db: Session, usuario_id: int):
    return db.query(models.Investimento).filter(models.Investimento.usuario_id == usuario_id).all()

# Transações
def create_transacao(db: Session, transacao: schemas.TransacaoCreate, usuario_id: int):
    nova = models.Transacao(
        tipo=transacao.tipo,
        quantidade=transacao.quantidade,
        preco=transacao.preco,
        data=transacao.data,
        investimento_id=transacao.investimento_id,
        usuario_id=usuario_id
    )
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

def get_transacoes_by_usuario(db: Session, usuario_id: int):
    return db.query(models.Transacao).filter(models.Transacao.usuario_id == usuario_id).all()

# Relatório
def gerar_relatorio_carteira(db: Session, usuario_id: int):
    investimentos = get_investimentos_by_usuario(db, usuario_id)
    transacoes = get_transacoes_by_usuario(db, usuario_id)

    total_investido = sum(t.quantidade * t.preco for t in transacoes if t.tipo == "compra")
    saldo_atual = sum(inv.valor for inv in investimentos)
    rentabilidade = ((saldo_atual - total_investido) / total_investido * 100) if total_investido > 0 else 0.0

    return schemas.RelatorioCarteira(
        total_investido=total_investido,
        saldo_atual=saldo_atual,
        rentabilidade=rentabilidade,
        quantidade_transacoes=len(transacoes),
        investimentos=investimentos
    )

# Consultas
def create_consulta(db: Session, consulta: schemas.ConsultaCreate, usuario_id: int):
    nova = models.Consulta(
        ativos=consulta.ativos,
        periodo=consulta.periodo,
        data_consulta=consulta.data_consulta,
        usuario_id=usuario_id
    )
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

def get_consultas_by_usuario(db: Session, usuario_id: int):
    return db.query(models.Consulta).filter(models.Consulta.usuario_id == usuario_id).all()
