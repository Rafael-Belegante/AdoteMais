from datetime import datetime
from pydantic import BaseModel, ConfigDict


class LogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_log: int
    data_hora: datetime
    id_usuario: int | None = None
    acao: str
    detalhe: str | None = None
