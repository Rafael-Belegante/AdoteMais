from pydantic_settings import BaseSettings  # já ajustado pra Pydantic v2

class Settings(BaseSettings):
    PROJECT_NAME: str = "ADOTE+"
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    DATABASE_URL: str = "sqlite:///./adote_mais.db"
    JWT_SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 360

    # 👇 Admin padrão
    ADMIN_DEFAULT_EMAIL: str = "admin@adotemais.local"
    ADMIN_DEFAULT_PASSWORD: str = "Admin@123"  # troca depois em produção
    ADMIN_DEFAULT_NAME: str = "Administrador ADOTE+"

    class Config:
        env_file = ".env"

settings = Settings()
