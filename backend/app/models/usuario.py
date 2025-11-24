from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    telefone = Column(String, nullable=True)
    senha_hash = Column(String, nullable=False)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    tipo = Column(String, default="usuario")  # visitante (sem login não entra), usuario, ong, admin
