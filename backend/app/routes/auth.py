from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, get_current_user
from app.schemas.usuario import UsuarioCreate, UsuarioOut, Token
from app.services.usuario_service import create_user, authenticate_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/register", response_model=UsuarioOut)
def register_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    user = create_user(db, data)
    return user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    token = create_access_token({"sub": str(user.id_usuario), "tipo": user.tipo})
    return Token(access_token=token)

@router.get("/me", response_model=UsuarioOut)
def me(current_user: Usuario = Depends(get_current_user)):
    return current_user
