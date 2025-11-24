from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.mensagem import MensagemCreate, MensagemOut
from app.services.mensagens_service import criar_mensagem
from app.models.mensagem import Mensagem
from app.core.security import require_role

router = APIRouter(prefix="/mensagens", tags=["Mensagens"])

@router.post("/", response_model=MensagemOut)
def enviar_mensagem(data: MensagemCreate, db: Session = Depends(get_db)):
    return criar_mensagem(db, data)

@router.get("/", response_model=List[MensagemOut], dependencies=[Depends(require_role("ong", "admin"))])
def listar_mensagens(db: Session = Depends(get_db)):
    return db.query(Mensagem).all()
