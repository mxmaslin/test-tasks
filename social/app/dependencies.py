from functools import lru_cache

from redis import Redis, ConnectionPool
from sqlalchemy.orm import Session

from app.settings import settings
from app.models import SessionLocal


pool = ConnectionPool(
    host=settings().REDIS_HOST,
    port=settings().REDIS_PORT,
    db=0
)


@lru_cache
def get_redis() -> Redis:
    return Redis(connection_pool=pool)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()