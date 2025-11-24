from datetime import datetime
from pydantic import BaseModel

class AdocaoBase(BaseModel):
    id_usuario: int
    id_animal: int

class AdocaoCreate(AdocaoBase):
    pass

class AdocaoOut(AdocaoBase):
    id_adocao: int
    status: str
    data_solicitacao: datetime

    class Config:
        from_attributes = True
