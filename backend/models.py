from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)

    investimentos = relationship("Investimento", back_populates="usuario")
    transacoes = relationship("Transacao", back_populates="usuario")
    consultas = relationship("Consulta", back_populates="usuario")

class Investimento(Base):
    __tablename__ = "investimentos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    usuario = relationship("Usuario", back_populates="investimentos")
    transacoes = relationship("Transacao", back_populates="investimento")

class Transacao(Base):
    __tablename__ = "transacoes"
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco = Column(Float, nullable=False)
    data = Column(Date, nullable=False)
    investimento_id = Column(Integer, ForeignKey("investimentos.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    investimento = relationship("Investimento", back_populates="transacoes")
    usuario = relationship("Usuario", back_populates="transacoes")

class Consulta(Base):
    __tablename__ = "consultas"
    id = Column(Integer, primary_key=True, index=True)
    ativos = Column(String, nullable=False)
    periodo = Column(String, nullable=False)
    data_consulta = Column(Date, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    usuario = relationship("Usuario", back_populates="consultas")
