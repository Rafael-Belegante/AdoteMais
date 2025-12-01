from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings
from app.core.database import Base, engine, SessionLocal
from app.middleware.security_headers import SecurityHeadersMiddleware
from app import models  # noqa: F401  # garante registro das tabelas

from app.routes import auth, animais, adocoes, usuarios, logs, uploads
from app.services.usuario_service import get_user_by_email, create_admin_user


def init_admin() -> None:
    """Cria usuário admin padrão se não existir."""
    db = SessionLocal()
    try:
        admin = get_user_by_email(db, settings.ADMIN_DEFAULT_EMAIL)
        if not admin:
            create_admin_user(
                db,
                nome=settings.ADMIN_DEFAULT_NAME,
                email=settings.ADMIN_DEFAULT_EMAIL,
                senha=settings.ADMIN_DEFAULT_PASSWORD,
            )
            print(f"Usuário admin padrão criado: {settings.ADMIN_DEFAULT_EMAIL}")
        else:
            print(f"Usuário admin padrão já existe: {settings.ADMIN_DEFAULT_EMAIL}")
    finally:
        db.close()


app = FastAPI(title=settings.PROJECT_NAME)


@app.on_event("startup")
def on_startup() -> None:
    """
    Inicializa o schema do banco e o usuário admin na subida da aplicação.

    Obs.: Em produção, o ideal é usar migrações (Alembic) em vez de create_all.
    """
    Base.metadata.create_all(bind=engine)
    init_admin()


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/media", StaticFiles(directory=UPLOAD_DIR), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SecurityHeadersMiddleware)

app.include_router(auth.router)
app.include_router(animais.router)
app.include_router(adocoes.router)
app.include_router(usuarios.router)
app.include_router(logs.router)
app.include_router(uploads.router)


@app.get("/")
def root():
    return {"msg": "API ADOTE+ ativa"}
