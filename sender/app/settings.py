from pydantic import BaseSettings


class Settings(BaseSettings):
    FLASK_DEBUG: bool
    DATABASE_URL: str
    SECRET_KEY: str
    LOG_LEVEL: str = 'DEBUG'
    API_VERSION: str = 1
    SENDER_URL: str
    SENDER_TOKEN: str


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
