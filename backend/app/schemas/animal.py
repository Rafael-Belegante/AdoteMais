from datetime import datetime
from pydantic import BaseModel, ConfigDict


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
    """Dados para criação de animal pelo anunciante."""
    pass


class AnimalUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    porte: str | None = None
    idade: int | None = None
    sexo: str | None = None
    raca: str | None = None
    especie: str | None = None
    foto_url: str | None = None
    status: str | None = None


class AnimalOut(AnimalBase):
    model_config = ConfigDict(from_attributes=True)

    id_animal: int
    status: str
    data_encontrado: datetime
