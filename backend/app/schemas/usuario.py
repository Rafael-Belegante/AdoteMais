from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: str | None = None


class UsuarioCreate(UsuarioBase):
    senha: str
    # cadastro público só permite usuario ou anunciante (mas o service ainda força tipo="usuario")
    tipo: Literal["usuario", "anunciante"] = "usuario"


class UsuarioAdminCreate(UsuarioBase):
    senha: str
    # admin pode criar qualquer tipo
    tipo: Literal["usuario", "anunciante", "admin"] = "usuario"


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    senha: Optional[str] = None
    tipo: Optional[Literal["usuario", "anunciante", "admin"]] = None


class UsuarioOut(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)

    id_usuario: int
    tipo: str
    data_cadastro: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PerfilUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
