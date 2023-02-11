from typing import Optional

from pydantic import BaseModel, Field, validator

from models import StringValidator


class UserBase(BaseModel):
    phone_number: str = Field(min_length=11, max_length=11)

    @validator('phone_number')
    def validate_phone_number(cls, value):
        return StringValidator.is_valid_phone_number(value)



class UserGet(UserBase):
    ...


class UserDelete(UserBase):
    ...


class UserCreate(UserBase):
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    patronymic: str = Optional[str]
    email: str = Optional[str]
    country: str = Field(max_length=50)

    @validator('name')
    def validate_name(cls, value):
        return StringValidator.is_cyrillic_plus(value)

    @validator('surname')
    def validate_surname(cls, value):
        return StringValidator.is_cyrillic_plus(value)

    @validator('patronymic')
    def validate_patronymic(cls, value):
        if value:
            return StringValidator.is_cyrillic_plus(value)

    @validator('email')
    def validate_email(cls, value):
        if value:
            return StringValidator.is_valid_email(value)

    @validator('country')
    def validate_country(cls, value):
        return StringValidator.is_cyrillic_plus(value)
