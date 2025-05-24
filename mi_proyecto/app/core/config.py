from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mysql_user: str
    mysql_password: str
    mysql_database: str
    mysql_root_password: str
    sentry_dsn: str = ""  # Opcional para que no falle en desarrollo sin Sentry

    class Config:
        env_file = ".env"

settings = Settings()
