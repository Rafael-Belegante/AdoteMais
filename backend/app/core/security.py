from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

from app.core.config import settings
from app.core.database import get_db
from app.models.usuario import Usuario

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    """Gera hash seguro da senha."""
    if len(password) > 128:
        raise HTTPException(status_code=400, detail="Senha muito longa.")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria token de acesso JWT.

    Esperado: data deve conter pelo menos {"sub": <id_usuario str>} ou similar.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        raw_sub = payload.get("sub")
        if raw_sub is None:
            raise credentials_exception

        try:
            user_id = int(raw_sub)
        except (TypeError, ValueError):
            # Token malformado
            raise credentials_exception
    except JWTError:
        # Token inválido ou expirado
        raise credentials_exception

    user = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
    if user is None:
        raise credentials_exception
    return user


def require_role(*roles: str):
    allowed = set(roles)

    def wrapper(current_user: Usuario = Depends(get_current_user)) -> Usuario:
        if current_user.tipo not in allowed:
            raise HTTPException(status_code=403, detail="Permissão negada")
        return current_user

    return wrapper
