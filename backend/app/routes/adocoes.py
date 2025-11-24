from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.adocao import AdocaoCreate, AdocaoOut
from app.services.adocao_service import solicitar_adocao, alterar_status, listar_pendentes
from app.core.security import require_role

router = APIRouter(prefix="/adocoes", tags=["Adoções"])

@router.post("/", response_model=AdocaoOut, dependencies=[Depends(require_role("usuario", "admin"))])
def solicitar(data: AdocaoCreate, db: Session = Depends(get_db)):
    return solicitar_adocao(db, data)

@router.get("/pendentes", response_model=List[AdocaoOut], dependencies=[Depends(require_role("ong", "admin"))])
def pendentes(db: Session = Depends(get_db)):
    return listar_pendentes(db)

@router.put("/{id_adocao}/aprovar", response_model=AdocaoOut, dependencies=[Depends(require_role("ong", "admin"))])
def aprovar(id_adocao: int, db: Session = Depends(get_db)):
    return alterar_status(db, id_adocao, "aprovado")

@router.put("/{id_adocao}/negar", response_model=AdocaoOut, dependencies=[Depends(require_role("ong", "admin"))])
def negar(id_adocao: int, db: Session = Depends(get_db)):
    return alterar_status(db, id_adocao, "negado")
