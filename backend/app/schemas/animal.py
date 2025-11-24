from datetime import datetime
from pydantic import BaseModel

class AnimalBase(BaseModel):
    nome: str
    descricao: str | None = None
    porte: str | None = None
    idade: int | None = None
    sexo: str | None = None
    raca: str | None = None
    especie: str | None = None
    foto_url: str | None = None

class AnimalCreate(AnimalBase):
    id_ong: int | None = None

class AnimalOut(AnimalBase):
    id_animal: int
    status: str
    data_encontrado: datetime

    class Config:
        from_attributes = True
