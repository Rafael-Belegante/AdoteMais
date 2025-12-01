from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.adocao import Adocao
from app.models.animal import Animal


def solicitar_adocao(db: Session, id_usuario: int, id_animal: int) -> Adocao:
    """
    USUARIO solicita adoção de um animal disponível.
    """
    animal = db.query(Animal).filter(Animal.id_animal == id_animal).first()
    if not animal or animal.status != "disponivel":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Animal indisponível para adoção",
        )

    # opcional: impedir que o anunciante adote o próprio animal
    if animal.id_anunciante == id_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível adotar um animal que você mesmo anunciou",
        )

    animal.status = "aguardando_aprovacao"

    adocao = Adocao(
        id_usuario=id_usuario,
        id_animal=id_animal,
        # data_solicitacao e status vêm pelos defaults
        # data_resposta fica NULL até a decisão
    )
    db.add(adocao)
    db.commit()
    db.refresh(adocao)
    return adocao


def listar_pendentes_para_anunciante(db: Session, id_anunciante: int) -> list[Adocao]:
    """
    Lista adoções pendentes para os animais de um anunciante específico.
    """
    return (
        db.query(Adocao)
        .join(Animal, Adocao.id_animal == Animal.id_animal)
        .filter(
            Animal.id_anunciante == id_anunciante,
            Adocao.status == "pendente",
        )
        .order_by(Adocao.data_solicitacao.desc())
        .all()
    )


def alterar_status(
    db: Session,
    id_adocao: int,
    novo_status: str,
    id_executor: int,
    is_admin: bool = False,
    mensagem_anunciante: str | None = None,
) -> Adocao:
    """
    Altera status de uma adoção (aprovado/negado) e atualiza o status do animal.
    `id_executor` é o usuário que está decidindo (anunciante ou admin).
    """
    adocao = db.query(Adocao).filter(Adocao.id_adocao == id_adocao).first()
    if not adocao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solicitação não encontrada",
        )

    if novo_status not in {"aprovado", "negado"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status inválido",
        )

    if adocao.status != "pendente":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Somente solicitações pendentes podem ser alteradas",
        )

    animal = db.query(Animal).filter(Animal.id_animal == adocao.id_animal).first()
    if not animal:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Animal associado não encontrado",
        )

    # segurança: anunciante só decide sobre seus animais; admin sobre qualquer um
    if not is_admin and animal.id_anunciante != id_executor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não pode alterar esta solicitação de adoção",
        )

    adocao.status = novo_status
    adocao.mensagem_anunciante = mensagem_anunciante
    adocao.data_resposta = datetime.utcnow()  # <<< MOMENTO DA RESPOSTA

    if novo_status == "aprovado":
        animal.status = "adotado"
    else:
        animal.status = "disponivel"

    db.commit()
    db.refresh(adocao)
    return adocao


def listar_minhas_adocoes(db: Session, id_usuario: int) -> list[Adocao]:
    """
    Lista adoções feitas por um usuário.
    """
    return (
        db.query(Adocao)
        .filter(Adocao.id_usuario == id_usuario)
        .order_by(Adocao.data_solicitacao.desc())
        .all()
    )
