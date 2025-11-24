from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine, SessionLocal
from app.middleware.security_headers import SecurityHeadersMiddleware
from app import models  # garante registro das tabelas

from app.routes import auth, animais, adocoes, mensagens, usuarios
from app.services.usuario_service import get_user_by_email, create_admin_user

# Cria tabelas
Base.metadata.create_all(bind=engine)


def init_admin():
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
            print("Usuário admin padrão criado:", settings.ADMIN_DEFAULT_EMAIL)
        else:
            print("Usuário admin padrão já existe:", settings.ADMIN_DEFAULT_EMAIL)
    finally:
        db.close()


# Inicializa admin na subida da aplicação
init_admin()

app = FastAPI(title=settings.PROJECT_NAME)

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
app.include_router(mensagens.router)
app.include_router(usuarios.router)


@app.get("/")
def root():
    return {"msg": "API ADOTE+ ativa"}
