from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.animal import AnimalOut, AnimalCreate
from app.services.animais_service import listar_disponiveis, criar_animal
from app.core.security import require_role
from app.models.animal import Animal

router = APIRouter(prefix="/animais", tags=["Animais"])

@router.get("/", response_model=List[AnimalOut])
def listar_animais(db: Session = Depends(get_db)):
    return listar_disponiveis(db)

@router.get("/{id_animal}", response_model=AnimalOut)
def obter_animal(id_animal: int, db: Session = Depends(get_db)):
    animal = db.query(Animal).filter(Animal.id_animal == id_animal).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal não encontrado")
    return animal

@router.post("/", response_model=AnimalOut, dependencies=[Depends(require_role("ong", "admin"))])
def cadastrar_animal(data: AnimalCreate, db: Session = Depends(get_db)):
    return criar_animal(db, data)
