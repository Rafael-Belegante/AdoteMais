from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Adocao(Base):
    __tablename__ = "adocoes"

    id_adocao = Column(Integer, primary_key=True, index=True)

    # quando o usuário solicita
    data_solicitacao = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # pendente, aprovado, negado
    status = Column(String(20), default="pendente", nullable=False, index=True)

    # mensagem opcional do ANUNCIANTE (justificando aprovação/negação)
    mensagem_anunciante = Column(String(500), nullable=True)

    # data em que o ANUNCIANTE deu a resposta (só é preenchida em aprovado/negado)
    data_resposta = Column(DateTime, nullable=True)  # <<< AGORA PODE SER NULL

    id_usuario = Column(
        Integer,
        ForeignKey("usuarios.id_usuario", ondelete="CASCADE"),
        nullable=False,
    )
    id_animal = Column(
        Integer,
        ForeignKey("animais.id_animal", ondelete="CASCADE"),
        nullable=False,
    )

    # Esses back_populates exigem que Usuario/Animal também tenham relationship("Adocao", back_populates="...")
    usuario = relationship(
        "Usuario",
        back_populates="adocoes",
        lazy="joined",
    )

    animal = relationship(
        "Animal",
        back_populates="adocoes",
        lazy="joined",
    )
