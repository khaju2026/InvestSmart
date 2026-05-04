from pydantic import BaseModel
from datetime import date

class UsuarioBase(BaseModel):
    nome: str
    email: str
    cpf: str

class UsuarioCreate(UsuarioBase):
    senha: str

class Usuario(UsuarioBase):
    id: int
    class Config:
        from_attributes = True

class InvestimentoBase(BaseModel):
    nome: str
    valor: float

class InvestimentoCreate(InvestimentoBase):
    usuario_id: int

class Investimento(InvestimentoBase):
    id: int
    usuario_id: int
    class Config:
        from_attributes = True

class TransacaoBase(BaseModel):
    tipo: str
    quantidade: int
    preco: float
    data: date

class TransacaoCreate(TransacaoBase):
    investimento_id: int
    usuario_id: int

class Transacao(TransacaoBase):
    id: int
    investimento_id: int
    usuario_id: int
    class Config:
        from_attributes = True

class ConsultaBase(BaseModel):
    ativos: str
    periodo: str
    data_consulta: date

class ConsultaCreate(ConsultaBase):
    usuario_id: int

class Consulta(ConsultaBase):
    id: int
    usuario_id: int
    class Config:
        from_attributes = True

class RelatorioCarteira(BaseModel):
    total_investido: float
    saldo_atual: float
    rentabilidade: float
    quantidade_transacoes: int
    investimentos: list[Investimento]
    darf: float = 0.0
