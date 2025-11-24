from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.core.security import hash_password, verify_password


def get_user_by_email(db: Session, email: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.email == email).first()


def create_user(db: Session, data: UsuarioCreate) -> Usuario:
    if get_user_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    # Garante que o tipo seja apenas usuario ou ong (segurança)
    tipo = data.tipo if data.tipo in ("usuario", "ong") else "usuario"

    user = Usuario(
        nome=data.nome,
        email=data.email,
        telefone=data.telefone,
        senha_hash=hash_password(data.senha),
        tipo=tipo,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, senha: str) -> Usuario | None:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(senha, user.senha_hash):
        return None
    return user


def create_admin_user(db: Session, nome: str, email: str, senha: str) -> Usuario:
    if get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    user = Usuario(
        nome=nome,
        email=email,
        telefone=None,
        senha_hash=hash_password(senha),
        tipo="admin",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
