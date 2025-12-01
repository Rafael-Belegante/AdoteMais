from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, get_current_user
from app.schemas.usuario import UsuarioCreate, UsuarioOut, Token, PerfilUpdate
from app.services import usuario_service
from app.services.log_service import registrar_log
from app.models.usuario import Usuario

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/register", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def register_usuario(
    data: UsuarioCreate,
    db: Session = Depends(get_db),
):
    """
    Registro público de usuário do tipo 'usuario' por padrão.
    """
    user = usuario_service.create_user_public(db, data)

    registrar_log(
        db,
        id_usuario=user.id_usuario,
        acao="usuario_registro",
        detalhe=f"Registro de usuário: {user.email}",
    )
    return user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Login com email (username) e senha.
    """
    user = usuario_service.authenticate_user(
        db,
        email=form_data.username,
        senha=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credenciais inválidas",
        )

    access_token = create_access_token(
        {"sub": str(user.id_usuario), "tipo": user.tipo}
    )

    registrar_log(
        db,
        id_usuario=user.id_usuario,
        acao="login",
        detalhe=f"Login realizado para {user.email}",
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UsuarioOut)
def me(current_user: Usuario = Depends(get_current_user)):
    """
    Retorna os dados do usuário autenticado.
    """
    return current_user


@router.put("/me", response_model=UsuarioOut)
def update_me(
    data: PerfilUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    if data.nome is not None:
        current_user.nome = data.nome
    if data.telefone is not None:
        current_user.telefone = data.telefone
    db.commit()
    db.refresh(current_user)
    return current_user
