import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "User Balance Service"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API для управления пользовательским балансом"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres")
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://auth-service.local/validate")
    AUTH_SERVICE_SECRET: str = os.getenv("AUTH_SERVICE_SECRET", "supersecretkey")
    GRPC_PORT: int = int(os.getenv("GRPC_PORT", 50051))
    HTTP_PORT: int = int(os.getenv("HTTP_PORT", 8000))
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

settings = Settings()