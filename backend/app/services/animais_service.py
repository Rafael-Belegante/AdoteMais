from sqlalchemy.orm import Session
from app.models.animal import Animal
from app.schemas.animal import AnimalCreate

def listar_disponiveis(db: Session):
    return db.query(Animal).filter(Animal.status == "disponivel").all()

def criar_animal(db: Session, data: AnimalCreate) -> Animal:
    animal = Animal(
        nome=data.nome,
        descricao=data.descricao,
        porte=data.porte,
        idade=data.idade,
        sexo=data.sexo,
        raca=data.raca,
        especie=data.especie,
        foto_url=data.foto_url,
        id_ong=data.id_ong,
    )
    db.add(animal)
    db.commit()
    db.refresh(animal)
    return animal
