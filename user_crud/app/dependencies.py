from functools import lru_cache

from dadata import Dadata
from redis import Redis, ConnectionPool
from sqlalchemy.orm import Session

from models import SessionLocal
from settings import settings


pool = ConnectionPool(
    host=settings().REDIS_HOST,
    port=settings().REDIS_PORT,
    db=0
)


@lru_cache
def get_redis() -> Redis:
    return Redis(connection_pool=pool)


def get_db() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@lru_cache
def get_dadata() -> Dadata:
    return Dadata(settings().DADATA_KEY)
