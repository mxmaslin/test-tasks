from pydantic import BaseSettings


class Settings(BaseSettings):
    API_VERSION: str = 1
    FLASK_DEBUG: bool
    SECRET_KEY: str
    LOG_LEVEL: str = 'DEBUG'


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')