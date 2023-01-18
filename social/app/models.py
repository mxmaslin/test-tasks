import asyncio

from peewee import Model, CharField, ForeignKeyField, TextField
from peewee_async import Manager, PostgresqlDatabase
from settings import settings


loop = asyncio.new_event_loop()
database = PostgresqlDatabase(
    settings().POSTGRES_DB,
    host=settings().POSTGRES_HOST,
    port=settings().POSTGRES_PORT,
    user=settings().POSTGRES_USER,
    password=settings().POSTGRES_PASSWORD
)
objects = Manager(database, loop=loop)
objects.database.allow_sync = False


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    email = CharField(unique=True)
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
