from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class LogAuditoria(Base):
    __tablename__ = "logs_auditoria"

    id_log = Column(Integer, primary_key=True, index=True)
    data_hora = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    acao = Column(String(50), nullable=False, index=True)
    detalhe = Column(String(1000), nullable=True)

    id_usuario = Column(
        Integer,
        ForeignKey("usuarios.id_usuario", ondelete="SET NULL"),
        nullable=True,
    )

    usuario = relationship(
        "Usuario",
        back_populates="logs",
        lazy="joined",
    )
