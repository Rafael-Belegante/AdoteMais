from datetime import datetime
from pydantic import BaseModel

class MensagemCreate(BaseModel):
    assunto: str
    mensagem: str
    telefone: str | None = None
    email_remetente: str | None = None
    nome_remetente: str | None = None
    id_ong: int | None = None

class MensagemOut(MensagemCreate):
    id_msg: int
    data_envio: datetime

    class Config:
        from_attributes = True
