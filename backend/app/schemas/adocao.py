from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AdocaoCreate(BaseModel):
    id_animal: int


class AdocaoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_adocao: int
    id_usuario: int
    id_animal: int
    status: str
    data_solicitacao: datetime
    mensagem_anunciante: str | None = None
    # opcional, se você adicionou esse campo no model Adocao
    data_resposta: datetime | None = None


class DecisaoAdocao(BaseModel):
    mensagem_anunciante: str | None = None
