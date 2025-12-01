from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_role
from app.models.usuario import Usuario
from app.schemas.adocao import AdocaoCreate, AdocaoOut, DecisaoAdocao
from app.services import adocao_service
from app.services.log_service import registrar_log

router = APIRouter(prefix="/adocoes", tags=["Adoções"])


@router.post("/", response_model=AdocaoOut, status_code=status.HTTP_201_CREATED)
def solicitar(
    data: AdocaoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("usuario", "admin")),
):
    """
    Usuário (ou admin) solicita adoção de um animal.
    Front envia: { "id_animal": <int> }
    """
    adocao = adocao_service.solicitar_adocao(
        db,
        id_usuario=current_user.id_usuario,
        id_animal=data.id_animal,
    )

    registrar_log(
        db,
        id_usuario=current_user.id_usuario,
        acao="solicitar_adocao",
        detalhe=f"id_adocao={adocao.id_adocao}, id_animal={data.id_animal}",
    )
    return adocao


@router.get("/pendentes", response_model=List[AdocaoOut])
def pendentes_para_anunciante(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("anunciante", "admin")),
):
    """
    Lista adoções pendentes para o anunciante logado (ou admin).
    Usado no painel de pedidos do anunciante.
    """
    return adocao_service.listar_pendentes_para_anunciante(
        db,
        id_anunciante=current_user.id_usuario,
    )


@router.put("/{id_adocao}/aprovar", response_model=AdocaoOut)
def aprovar(
    id_adocao: int,
    body: DecisaoAdocao,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("anunciante", "admin")),
):
    """
    Anunciante aprova pedido de adoção.
    Mensagem é OBRIGATÓRIA.
    """
    msg = (body.mensagem_anunciante or "").strip()
    if not msg:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mensagem do anunciante é obrigatória para aprovar o pedido.",
        )

    adocao = adocao_service.alterar_status(
        db,
        id_adocao=id_adocao,
        novo_status="aprovado",
        id_executor=current_user.id_usuario,
        is_admin=current_user.tipo == "admin",
        mensagem_anunciante=msg,
    )

    registrar_log(
        db,
        id_usuario=current_user.id_usuario,
        acao="adocao_aprovar",
        detalhe=f"id_adocao={id_adocao}",
    )
    return adocao


@router.put("/{id_adocao}/negar", response_model=AdocaoOut)
def negar(
    id_adocao: int,
    body: DecisaoAdocao,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("anunciante", "admin")),
):
    """
    Anunciante nega pedido de adoção.
    Mensagem é OBRIGATÓRIA.
    """
    msg = (body.mensagem_anunciante or "").strip()
    if not msg:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mensagem do anunciante é obrigatória para negar o pedido.",
        )

    adocao = adocao_service.alterar_status(
        db,
        id_adocao=id_adocao,
        novo_status="negado",
        id_executor=current_user.id_usuario,
        is_admin=current_user.tipo == "admin",
        mensagem_anunciante=msg,
    )

    registrar_log(
        db,
        id_usuario=current_user.id_usuario,
        acao="adocao_negar",
        detalhe=f"id_adocao={id_adocao}",
    )
    return adocao


@router.get("/minhas", response_model=List[AdocaoOut])
def minhas_adocoes(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("usuario", "admin")),
):
    """
    Lista pedidos de adoção feitos pelo usuário logado.
    Usado em "Minhas Adoções" no painel do usuário.
    """
    return adocao_service.listar_minhas_adocoes(
        db,
        id_usuario=current_user.id_usuario,
    )
