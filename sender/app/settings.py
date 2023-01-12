from pathlib import Path
from pydantic import BaseSettings


class Settings(BaseSettings):
    FLASK_DEBUG: bool
    LOG_LEVEL: str = 'DEBUG'

    APP_HOST: str = 'localhost'
    APP_PORT: int = 5000

    REDIS_PORT: int = 6379

    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = 5432 
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    SECRET_KEY: str
    API_VERSION: str = 1
    SENDER_URL: str
    SENDER_TOKEN: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str


env = Path.cwd().joinpath('.env')
settings = Settings(_env_file=env, _env_file_encoding='utf-8')
