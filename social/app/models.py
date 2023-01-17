from peewee import *
from settings import settings


db = PostgresqlDatabase(
    settings().POSTGRES_DB,
    host=settings().POSTGRES_HOST,
    port=settings().POSTGRES_PORT,
    user=settings().POSTGRES_USER,
    password=settings().POSTGRES_PASSWORD
)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    email = CharField(unique=True)
    password_hash = CharField(null=True)

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)
    
    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)

    # @staticmethod
    # def login(email, password):
    #     person = User.get(User.email == email)
    #     if not person or not person.check_password(password):
    #         raise LoginFail
    #     return person


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
