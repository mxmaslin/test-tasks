import re
from fastapi import FastAPI
from pydantic import BaseModel, validator
from sqlalchemy import create_engine
from typing import Optional

db_name = 'database'
db_user = 'username'
db_pass = 'secret'
db_host = 'db'
db_port = '5432'

db_string = f'postgres://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
db = create_engine(db_string)




class Person(BaseModel):
    first_name: str
    patronymic: Optional[str] = None
    last_name: str
    sex: str
    country: str
    phone: str

    @validator('country', 'first_name', 'patronymic', 'last_name')
    def validate_alpha_value(cls, value):
        if value.isalpha():
            return value
        raise ValueError('Invalid value')

    @validator('sex')
    def validate_sex(cls, sex):
        if sex in ('m', 'f'):
            return sex
        raise ValueError('Invalid sex')

    @validator('phone')
    def validate_phone(cls, number):
        if re.match(r'7\d{3}\d{3}\d{2}\d{2}', number):
            return number
        raise ValueError('Invalid phone number')


# person = Person(
#     first_name='Maxim',
#     patronymic='Mikhailovitch',
#     last_name='Maslin',
#     sex='m',
#     phone='+7(123)111-22-33'
# )
#

app = FastAPI()


@app.post('/')
async def create_person(person: Person):
    return person


@app.get('/')
async def get_person():
    return {'person': 'Maxim'}