from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Animal(Base):
    __tablename__ = "animais"

    id_animal = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    descricao = Column(String(1000), nullable=True)
    porte = Column(String(50), nullable=True)
    idade = Column(Integer, nullable=True)
    sexo = Column(String(20), nullable=True)
    raca = Column(String(100), nullable=True)
    especie = Column(String(50), nullable=True)

    foto_url = Column(String(500), nullable=True)
    data_encontrado = Column(DateTime, default=datetime.utcnow, nullable=False)
    # valores: "disponivel", "aguardando_aprovacao", "adotado"
    status = Column(String(30), default="disponivel", nullable=False)

    id_anunciante = Column(
        Integer,
        ForeignKey("usuarios.id_usuario", ondelete="RESTRICT"),
        nullable=False,
    )

    # Relacionamentos
    anunciante = relationship(
        "Usuario",
        back_populates="animais_anunciados",
        lazy="joined",
    )

    adocoes = relationship(
        "Adocao",
        back_populates="animal",
        lazy="selectin",
    )
