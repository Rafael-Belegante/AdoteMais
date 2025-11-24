from sqlalchemy import Column, Integer, String
from app.core.database import Base

class ONG(Base):
    __tablename__ = "ongs"

    id_ong = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cnpj_cpf = Column(String, nullable=False)
    endereco = Column(String, nullable=True)
    telefone = Column(String, nullable=True)
    email = Column(String, nullable=True)
