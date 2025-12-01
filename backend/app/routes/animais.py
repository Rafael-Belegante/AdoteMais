from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_role
from app.models.animal import Animal
from app.models.usuario import Usuario
from app.schemas.animal import AnimalOut, AnimalCreate, AnimalUpdate
from app.services import animais_service
from app.services.log_service import registrar_log

router = APIRouter(prefix="/animais", tags=["Animais"])


@router.get("/", response_model=List[AnimalOut])
def listar_animais(
    especie: str | None = None,
    porte: str | None = None,
    sexo: str | None = None,
    q: str | None = None,
    db: Session = Depends(get_db),
):
    return animais_service.listar_disponiveis(
        db,
        especie=especie,
        porte=porte,
        sexo=sexo,
        q=q,
    )


@router.get("/meus", response_model=List[AnimalOut])
def meus_animais(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("anunciante")),
):
    return animais_service.listar_por_anunciante(
        db,
        id_anunciante=current_user.id_usuario,
    )


@router.get("/admin/todos", response_model=List[AnimalOut])
def todos_animais(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin")),
):
    return animais_service.listar_todos(db)


@router.get("/{id_animal}", response_model=AnimalOut)
def obter_animal(
    id_animal: int,
    db: Session = Depends(get_db),
):
    animal = db.query(Animal).filter(Animal.id_animal == id_animal).first()
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal não encontrado")
    return animal


@router.post("/", response_model=AnimalOut, status_code=status.HTTP_201_CREATED)
def cadastrar_animal(
    data: AnimalCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("anunciante", "admin")),
):
    animal = animais_service.criar_animal(
        db,
        data=data,
        id_anunciante=current_user.id_usuario,
    )

    registrar_log(
        db,
        id_usuario=current_user.id_usuario,
        acao="animal_criar",
        detalhe=f"id_animal={animal.id_animal}",
    )
    return animal


@router.put("/{id_animal}", response_model=AnimalOut)
def atualizar_animal(
    id_animal: int,
    data: AnimalUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("anunciante", "admin")),
):
    animal = animais_service.atualizar_animal(
        db,
        id_animal=id_animal,
        data=data,
        id_executor=current_user.id_usuario,
        is_admin=current_user.tipo == "admin",
    )

    registrar_log(
        db,
        id_usuario=current_user.id_usuario,
        acao="animal_editar",
        detalhe=f"id_animal={id_animal}",
    )
    return animal


@router.delete("/{id_animal}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_animal(
    id_animal: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("anunciante", "admin")),
):
    animais_service.deletar_animal(
        db,
        id_animal=id_animal,
        id_executor=current_user.id_usuario,
        is_admin=current_user.tipo == "admin",
    )

    registrar_log(
        db,
        id_usuario=current_user.id_usuario,
        acao="animal_excluir",
        detalhe=f"id_animal={id_animal}",
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
