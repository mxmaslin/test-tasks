from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseSettings
from functools import lru_cache


env_path = Path.cwd().joinpath('.env')
load_dotenv(env_path)


class Settings(BaseSettings):
    API_VERSION: str = 1
    LOG_LEVEL: str = 'DEBUG'

    POSTGRES_HOST: str = 'localhost'
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379

    APP_HOST: str = '0.0.0.0'
    APP_PORT: int = 5000

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    EMAILHUNTER_API_KEY: str
    EMAILHUNTER_URL: str = 'https://api.emailhunter.co/v1/verify?email={email}&api_key=${EMAILHUNTER_API_KEY}'

    class Config:
        env_file = env_path


@lru_cache()
def settings():
    return Settings()
