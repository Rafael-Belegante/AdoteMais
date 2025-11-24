from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.adocao import Adocao
from app.models.animal import Animal
from app.schemas.adocao import AdocaoCreate

def solicitar_adocao(db: Session, data: AdocaoCreate) -> Adocao:
    animal = db.query(Animal).filter(Animal.id_animal == data.id_animal).first()
    if not animal or animal.status != "disponivel":
        raise HTTPException(status_code=400, detail="Animal indisponível")

    animal.status = "aguardando_aprovacao"

    adocao = Adocao(
        id_usuario=data.id_usuario,
        id_animal=data.id_animal,
    )
    db.add(adocao)
    db.commit()
    db.refresh(adocao)
    return adocao

def listar_pendentes(db: Session):
    return db.query(Adocao).filter(Adocao.status == "pendente").all()

def alterar_status(db: Session, id_adocao: int, novo_status: str) -> Adocao:
    adocao = db.query(Adocao).filter(Adocao.id_adocao == id_adocao).first()
    if not adocao:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")

    if novo_status not in {"aprovado", "negado"}:
        raise HTTPException(status_code=400, detail="Status inválido")

    adocao.status = novo_status
    animal = db.query(Animal).filter(Animal.id_animal == adocao.id_animal).first()
    if novo_status == "aprovado":
        animal.status = "adotado"
    elif novo_status == "negado":
        animal.status = "disponivel"

    db.commit()
    db.refresh(adocao)
    return adocao
