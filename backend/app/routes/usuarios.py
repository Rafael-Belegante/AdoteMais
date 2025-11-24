from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.usuario import UsuarioOut
from app.models.usuario import Usuario
from app.core.security import require_role

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.get("/", response_model=List[UsuarioOut], dependencies=[Depends(require_role("admin"))])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@router.get("/{id_usuario}", response_model=UsuarioOut, dependencies=[Depends(require_role("ong", "admin"))])
def obter_usuario(id_usuario: int, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user
