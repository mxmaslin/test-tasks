from peewee import *
from settings import settings
from werkzeug.security import generate_password_hash, check_password_hash

from exceptions import LoginFail


db = PostgresqlDatabase(
    settings.POSTGRES_DB,
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    user=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD
)


class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    first_name = CharField()
    second_name = CharField()
    username = CharField(unique=True)
    password_hash = CharField()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def login(username, password):
        person = Person.get(Person.username == username)
        if not person or not person.check_password(password):
            raise LoginFail
        return person


class Apartment(BaseModel):
    room_number = IntegerField()


class Booking(BaseModel):
    start_date = DateField()
    end_date = DateField()
    person = ForeignKeyField(Person)
    apartment = ForeignKeyField(Apartment)
