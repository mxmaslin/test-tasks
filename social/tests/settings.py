from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings


env_path = Path.cwd().joinpath('.test.env')
load_dotenv(env_path)


class Settings(BaseSettings):
    API_VERSION: str = 1
    LOG_LEVEL: str = 'DEBUG'

    TEST_POSTGRES_HOST: str = 'localhost'
    TEST_POSTGRES_DB: str
    TEST_POSTGRES_PORT: int = 5433
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str

    TEST_REDIS_HOST: str = 'localhost'
    TEST_REDIS_PORT: int = 6380

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    EMAILHUNTER_API_KEY: str
    EMAILHUNTER_URL: str = 'https://api.emailhunter.co/v1/verify?email={email}&api_key={api_key}'

    class Config:
        env_file = env_path


@lru_cache()
def settings():
    return Settings()
