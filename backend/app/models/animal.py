from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.core.database import Base

class Animal(Base):
    __tablename__ = "animais"

    id_animal = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    porte = Column(String, nullable=True)
    idade = Column(Integer, nullable=True)
    sexo = Column(String, nullable=True)
    raca = Column(String, nullable=True)
    especie = Column(String, nullable=True)

    foto_url = Column(String, nullable=True)
    data_encontrado = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="disponivel")  # disponivel, aguardando_aprovacao, adotado

    id_ong = Column(Integer, ForeignKey("ongs.id_ong"), nullable=True)
