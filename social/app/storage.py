import asyncio

from functools import lru_cache

from peewee import Model, BooleanField, CharField, ForeignKeyField, TextField
from peewee_async import Manager, PostgresqlDatabase
from redis import Redis, ConnectionPool

from app.settings import settings


loop = asyncio.new_event_loop()
database = PostgresqlDatabase(
    settings().POSTGRES_DB,
    host=settings().POSTGRES_HOST,
    port=settings().POSTGRES_PORT,
    user=settings().POSTGRES_USER,
    password=settings().POSTGRES_PASSWORD
)
objects = Manager(database, loop=loop)
objects.database.allow_sync = False  # set to True to make db migrations

pool = ConnectionPool(
    host=settings().REDIS_HOST,
    port=settings().REDIS_PORT,
    db=0
)


@lru_cache
def get_redis() -> Redis:
    return Redis(connection_pool=pool)


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    email = CharField(unique=True)
    disabled = BooleanField(default=False)
    password_hash = CharField(null=True)


class Post(BaseModel):
    user = ForeignKeyField(User, backref='posts')
    title = CharField()
    content = TextField()


class Like(BaseModel):
    user = ForeignKeyField(User, backref='likes')
    post = ForeignKeyField(Post, backref='likes')


class Dislike(BaseModel):
    user = ForeignKeyField(User, backref='dislikes')
    post = ForeignKeyField(Post, backref='dislikes')
