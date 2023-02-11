import random
import re
import string
import sys

from pathlib import Path

from sqlalchemy import create_engine, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, validates
from sqlalchemy.sql import expression
from sqlalchemy.ext.declarative import declarative_base

app_path = Path.cwd().parent
sys.path.append(str(app_path))

from app.settings import settings
from constants import (
    INVALID_EMAIL, INVALID_NAME, INVALID_SURNAME, INVALID_PATRONYMIC, INVALID_COUNTRY, INVALID_EMAIL, INVALID_PHONE
)


engine = create_engine(settings().SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class StringValidator:
    @staticmethod
    def is_cyrillic_plus(string):
        return bool(re.match(r'^[\u0400-\u04FF \-]+$', string))

    @staticmethod
    def is_valid_phone_number(string):
        return bool(re.match(r'^7\d{10}$', string))

    @staticmethod
    def is_valid_email(string):
        return bool(re.match(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',
            string
        ))


def generate_user_id():
    return ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=12)
    )


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(
        String(12), unique=True, nullable=False, default=generate_user_id
    )
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    patronymic: Mapped[str] = mapped_column(String(50), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(11), index=True, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=True)
    country: Mapped[str] = mapped_column(String(50))
    date_created: Mapped[DateTime] = mapped_column(
        DateTime, default=expression.text('CURRENT_TIMESTAMP')
    )
    date_modified: Mapped[DateTime] = mapped_column(
        DateTime,
        default=expression.text('CURRENT_TIMESTAMP'),
        onupdate=expression.text('CURRENT_TIMESTAMP')
    )

    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if not StringValidator.is_valid_phone_number(value):
            raise ValueError(INVALID_PHONE.format(value))
        return value

    @validates('name')
    def validate_name(self, key, value):
        if not StringValidator.is_cyrillic_plus(value):
            raise ValueError(INVALID_NAME.format(value))
        return value

    @validates('surname')
    def validate_surname(self, key, value):
        if not StringValidator.is_cyrillic_plus(value):
            raise ValueError(INVALID_SURNAME.format(value))
        return value

    @validates('patronymic')
    def validate_patronymic(self, key, value):
        if not StringValidator.is_cyrillic_plus(value):
            raise ValueError(INVALID_PATRONYMIC.format(value))
        return value

    @validates('country')
    def validate_country(self, key, value):
        if not StringValidator.is_cyrillic_plus(value):
            raise ValueError(INVALID_COUNTRY.format(value))
        return value

    @validates('email')
    def validate_email(self, key, value):
        if not StringValidator.is_valid_email(value):
            raise ValueError(INVALID_EMAIL.format(value))
        return value
