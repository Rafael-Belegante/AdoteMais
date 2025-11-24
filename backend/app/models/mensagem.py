from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.core.database import Base

class Mensagem(Base):
    __tablename__ = "mensagens"

    id_msg = Column(Integer, primary_key=True, index=True)
    data_envio = Column(DateTime, default=datetime.utcnow)
    assunto = Column(String, nullable=False)
    mensagem = Column(String, nullable=False)
    telefone = Column(String, nullable=True)
    email_remetente = Column(String, nullable=True)
    nome_remetente = Column(String, nullable=True)
    id_ong = Column(Integer, ForeignKey("ongs.id_ong"), nullable=True)
