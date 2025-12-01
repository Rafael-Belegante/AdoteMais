from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.usuario import Usuario
from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioAdminCreate,
    UsuarioUpdate,
)


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def get_user_by_email(db: Session, email: str) -> Usuario | None:
    email_norm = _normalize_email(email)
    return db.query(Usuario).filter(Usuario.email == email_norm).first()


def get_user_by_id(db: Session, id_usuario: int) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()


def listar_usuarios(db: Session) -> list[Usuario]:
    return db.query(Usuario).order_by(Usuario.data_cadastro.desc()).all()


def create_user_public(db: Session, data: UsuarioCreate) -> Usuario:
    """
    Criação de usuário pelo endpoint público (/auth/register).
    Sempre cria com tipo 'usuario'.
    """
    email_norm = _normalize_email(data.email)

    if get_user_by_email(db, email_norm):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado",
        )

    user = Usuario(
        nome=data.nome,
        email=email_norm,
        telefone=data.telefone,
        senha_hash=hash_password(data.senha),
        tipo="usuario",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_user(
    db: Session,
    data: UsuarioCreate,
    tipo_forcado: str | None = None,
) -> Usuario:
    """
    Criação genérica (se quiser reaproveitar).
    """
    email_norm = _normalize_email(data.email)

    if get_user_by_email(db, email_norm):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado",
        )

    if tipo_forcado in ("usuario", "anunciante"):
        tipo = tipo_forcado
    else:
        tipo = data.tipo if getattr(data, "tipo", None) in ("usuario", "anunciante") else "usuario"

    user = Usuario(
        nome=data.nome,
        email=email_norm,
        telefone=data.telefone,
        senha_hash=hash_password(data.senha),
        tipo=tipo,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_user_public(db: Session, data: UsuarioCreate) -> Usuario:
    email_norm = _normalize_email(data.email)

    if get_user_by_email(db, email_norm):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado",
        )

    tipo = data.tipo if data.tipo in ("usuario", "anunciante") else "usuario"

    user = Usuario(
        nome=data.nome,
        email=email_norm,
        telefone=data.telefone,
        senha_hash=hash_password(data.senha),
        tipo=tipo,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user



def atualizar_usuario(
    db: Session,
    id_usuario: int,
    data: UsuarioUpdate,
) -> Usuario:
    user = get_user_by_id(db, id_usuario)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )

    update_data = data.model_dump(exclude_unset=True)

    # email
    if "email" in update_data:
        email_norm = _normalize_email(update_data["email"])
        existing = get_user_by_email(db, email_norm)
        if existing and existing.id_usuario != id_usuario:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="E-mail já cadastrado",
            )
        user.email = email_norm
        update_data.pop("email")

    # senha
    if "senha" in update_data:
        user.senha_hash = hash_password(update_data["senha"])
        update_data.pop("senha")

    # tipo
    if "tipo" in update_data:
        tipo = update_data["tipo"]
        if tipo not in ("usuario", "anunciante", "admin"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo de usuário inválido",
            )
        user.tipo = tipo
        update_data.pop("tipo")

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def deletar_usuario(db: Session, id_usuario: int) -> None:
    user = get_user_by_id(db, id_usuario)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )
    db.delete(user)
    db.commit()


def authenticate_user(db: Session, email: str, senha: str) -> Usuario | None:
    email_norm = _normalize_email(email)
    user = get_user_by_email(db, email_norm)
    if not user:
        return None
    if not verify_password(senha, user.senha_hash):
        return None
    return user


def create_admin_user(db: Session, nome: str, email: str, senha: str) -> Usuario:
    """
    Cria admin padrão (usado no startup).
    """
    email_norm = _normalize_email(email)

    if get_user_by_email(db, email_norm):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado",
        )

    user = Usuario(
        nome=nome,
        email=email_norm,
        telefone=None,
        senha_hash=hash_password(senha),
        tipo="admin",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
