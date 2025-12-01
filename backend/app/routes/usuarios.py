from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_role
from app.models.usuario import Usuario
from app.schemas.usuario import (
    UsuarioOut,
    UsuarioAdminCreate,
    UsuarioUpdate,
)
from app.services import usuario_service
from app.services.log_service import registrar_log

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.get("/", response_model=List[UsuarioOut])
def listar_usuarios(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin")),
):
    return usuario_service.listar_usuarios(db)


@router.get("/{id_usuario}", response_model=UsuarioOut)
def obter_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin", "anunciante", "usuario")),
):
    user = usuario_service.get_user_by_id(db, id_usuario)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return user


@router.post("/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def criar_usuario(
    data: UsuarioAdminCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin")),
):
    user = usuario_service.create_user_admin(db, data)

    registrar_log(
        db,
        id_usuario=current_user.id_usuario,
        acao="usuario_criar",
        detalhe=f"id_usuario={user.id_usuario}, tipo={user.tipo}",
    )
    return user


@router.put("/{id_usuario}", response_model=UsuarioOut)
def atualizar_usuario(
    id_usuario: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin")),
):
    user = usuario_service.atualizar_usuario(db, id_usuario, data)

    registrar_log(
        db,
        id_usuario=current_user.id_usuario,
        acao="usuario_atualizar",
        detalhe=f"id_usuario={id_usuario}",
    )
    return user


@router.delete("/{id_usuario}", status_code=status.HTTP_200_OK)
def deletar_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin")),
):
    usuario_service.deletar_usuario(db, id_usuario)

    registrar_log(
        db,
        id_usuario=current_user.id_usuario,
        acao="usuario_excluir",
        detalhe=f"id_usuario={id_usuario}",
    )
    return {"detail": "Usuário removido com sucesso"}
