from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sentry_dsn: str = ""
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        extra = 'ignore'  # Allow and ignore extra fields from .env


settings = Settings()
