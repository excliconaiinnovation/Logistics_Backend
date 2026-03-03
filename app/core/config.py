from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()

# app/core/config.py

SECRET_KEY = "super_secret_key_change_this_123456"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


# SMTP CONFIG
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = "your_email@gmail.com"
SMTP_PASSWORD = "your_app_password"
FRONTEND_URL = "http://localhost:5173"