from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    telefone = Column(String(50), nullable=True)
    senha_hash = Column(String(255), nullable=False)
    data_cadastro = Column(DateTime, default=datetime.utcnow, nullable=False)
    # valores: "usuario", "anunciante", "admin"
    tipo = Column(String(20), default="usuario", nullable=False)

    # Relacionamentos
    animais_anunciados = relationship(
        "Animal",
        back_populates="anunciante",
        lazy="selectin",
    )

    adocoes = relationship(
        "Adocao",
        back_populates="usuario",
        lazy="selectin",
    )

    logs = relationship(
        "LogAuditoria",
        back_populates="usuario",
        lazy="selectin",
    )
