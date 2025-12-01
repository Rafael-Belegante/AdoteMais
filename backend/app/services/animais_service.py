from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.animal import Animal
from app.schemas.animal import AnimalCreate, AnimalUpdate


def listar_disponiveis(
    db: Session,
    especie: str | None = None,
    porte: str | None = None,
    sexo: str | None = None,
    q: str | None = None,
) -> list[Animal]:
    """
    Lista animais com status 'disponivel', com filtros opcionais.
    """
    query = db.query(Animal).filter(Animal.status == "disponivel")

    if especie:
        query = query.filter(Animal.especie.ilike(f"%{especie}%"))
    if porte:
        query = query.filter(Animal.porte.ilike(f"%{porte}%"))
    if sexo:
        query = query.filter(Animal.sexo.ilike(f"%{sexo}%"))
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                Animal.nome.ilike(like),
                Animal.descricao.ilike(like),
                Animal.raca.ilike(like),
            )
        )

    return query.order_by(Animal.data_encontrado.desc()).all()


def listar_por_anunciante(db: Session, id_anunciante: int) -> list[Animal]:
    return (
        db.query(Animal)
        .filter(Animal.id_anunciante == id_anunciante)
        .order_by(Animal.data_encontrado.desc())
        .all()
    )


def listar_todos(db: Session) -> list[Animal]:
    return db.query(Animal).order_by(Animal.data_encontrado.desc()).all()


def criar_animal(
    db: Session,
    data: AnimalCreate,
    id_anunciante: int,
) -> Animal:
    """
    Cria animal associado ao anunciante autenticado.
    Não aceita id_anunciante vindo do payload.
    """
    animal = Animal(
        nome=data.nome,
        descricao=data.descricao,
        porte=data.porte,
        idade=data.idade,
        sexo=data.sexo,
        raca=data.raca,
        especie=data.especie,
        foto_url=data.foto_url,
        id_anunciante=id_anunciante,
    )
    db.add(animal)
    db.commit()
    db.refresh(animal)
    return animal


def atualizar_animal(
    db: Session,
    id_animal: int,
    data: AnimalUpdate,
    id_executor: int,
    is_admin: bool = False,
) -> Animal:
    """
    Atualiza dados de um animal.
    Anunciante só pode alterar os próprios animais; admin pode alterar qualquer um.
    """
    animal = db.query(Animal).filter(Animal.id_animal == id_animal).first()
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal não encontrado")

    if not is_admin and animal.id_anunciante != id_executor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não pode alterar este animal",
        )

    update_data = data.model_dump(exclude_unset=True)

    # status com validação simples
    if "status" in update_data:
        novo_status = update_data["status"]
        if novo_status not in {"disponivel", "aguardando_aprovacao", "adotado"}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status de animal inválido",
            )
        animal.status = novo_status
        update_data.pop("status")

    for field, value in update_data.items():
        setattr(animal, field, value)

    db.commit()
    db.refresh(animal)
    return animal


def deletar_animal(
    db: Session,
    id_animal: int,
    id_executor: int,
    is_admin: bool = False,
) -> None:
    """
    Remove um animal.
    Anunciante só pode remover animais próprios; admin pode remover qualquer um.
    """
    animal = db.query(Animal).filter(Animal.id_animal == id_animal).first()
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal não encontrado")

    if not is_admin and animal.id_anunciante != id_executor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não pode remover este animal",
        )

    db.delete(animal)
    db.commit()
