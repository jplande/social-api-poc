from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Social API POC"
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24h

    # Database
    DATABASE_URL: str = "postgresql+psycopg://social_user:social_password@localhost:5432/social_db"

    class Config:
        env_file = ".env"

settings = Settings()