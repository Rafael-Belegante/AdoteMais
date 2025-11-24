from datetime import datetime
from typing import Literal
from pydantic import BaseModel, EmailStr


class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: str | None = None


class UsuarioCreate(UsuarioBase):
    senha: str
    tipo: Literal["usuario", "ong"] = "usuario"   # 👈 adotante ou ONG/voluntário


class UsuarioOut(UsuarioBase):
    id_usuario: int
    tipo: str
    data_cadastro: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
