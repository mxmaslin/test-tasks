from pydantic import BaseSettings


class Settings(BaseSettings):
    API_VERSION: str = 1
    FLASK_DEBUG: bool = True
    SECRET_KEY: str
    LOG_LEVEL: str = 'DEBUG'

    POSTGRES_HOST: str = 'localhost'
    POSTGRES_DB: str
    POSTGRES_PORT: str = '5432'
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    APP_HOST: str = '0.0.0.0'
    APP_PORT: str = '5000'


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')