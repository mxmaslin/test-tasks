from typing import Optional

from pydantic import BaseModel, Field, validator, constr

from models import StringValidator
from constants import (
    INVALID_EMAIL, INVALID_NAME, INVALID_SURNAME, INVALID_PATRONYMIC, INVALID_COUNTRY, INVALID_EMAIL, INVALID_PHONE
)


class UserBase(BaseModel):
    phone_number: constr(min_length=11, max_length=11)

    @validator('phone_number')
    def validate_phone_number(cls, value):
        if StringValidator.is_valid_phone_number(value):
            return value
        raise ValueError(INVALID_PHONE.format(value))


class UserGet(UserBase):
    ...


class UserDelete(UserBase):
    ...


class UserCreate(UserBase):
    name: constr(max_length=50)
    surname: constr(max_length=50)
    patronymic: Optional[str]
    email: Optional[str]
    country: constr(max_length=50)

    @validator('name')
    def validate_name(cls, value):
        if StringValidator.is_cyrillic_plus(value):
            return value
        raise ValueError(INVALID_NAME.format(value))
        
    @validator('surname')
    def validate_surname(cls, value):
        if StringValidator.is_cyrillic_plus(value):
            return value
        raise ValueError(INVALID_SURNAME.format(value))

    @validator('patronymic')
    def validate_patronymic(cls, value):
        if StringValidator.is_cyrillic_plus(value):
            return value
        raise ValueError(INVALID_PATRONYMIC.format(value))

    @validator('email')
    def validate_email(cls, value):
        if StringValidator.is_valid_email(value):
            return value
        raise ValueError(INVALID_EMAIL.format(value))

    @validator('country')
    def validate_country(cls, value):
        if StringValidator.is_cyrillic_plus(value):
            return value
        raise ValueError(INVALID_COUNTRY.format(value))