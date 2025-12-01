from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_role
from app.models.usuario import Usuario
from app.schemas.log import LogOut
from app.services.log_service import listar_logs

router = APIRouter(prefix="/logs", tags=["Auditoria"])


@router.get("/", response_model=List[LogOut])
def listar(
    id_usuario: int | None = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin")),
):
    """
    ADMIN visualiza logs de auditoria.
    Pode filtrar por id_usuario (?id_usuario=123).
    """
    return listar_logs(db, id_usuario=id_usuario)
