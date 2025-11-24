from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.core.database import Base

class Adocao(Base):
    __tablename__ = "adocoes"

    id_adocao = Column(Integer, primary_key=True, index=True)
    data_solicitacao = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pendente")  # pendente, aprovado, negado

    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_animal = Column(Integer, ForeignKey("animais.id_animal"), nullable=False)
