import re

from sqlalchemy import create_engine, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, validates
from sqlalchemy.sql import expression
from sqlalchemy.ext.declarative import declarative_base

from app.settings import settings


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
            r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            string
        ))


class User(Base):
    __tablename__ = 'users'
    
    user_id: Mapped[int] = mapped_column(String(12), primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    patronymic: Mapped[str] = mapped_column(String(50), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(11))
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
    def validate_phone_number(self, key, phone_number):
        if not StringValidator.is_valid_phone_number(phone_number):
            raise ValueError(f'{phone_number} is not a valid ru phone number')
        return phone_number

    @validates('name')
    def validate_name(self, key, name):
        if not StringValidator.is_cyrillic_plus(name):
            raise ValueError(f'{name} is not a valid ru name')
        return name

    @validates('surname')
    def validate_surname(self, key, surname):
        if not StringValidator.is_cyrillic_plus(surname):
            raise ValueError(f'{surname} is not a valid ru surname')
        return surname

    @validates('patronymic')
    def validate_patronymic(self, key, patronymic):
        if not StringValidator.is_cyrillic_plus(patronymic):
            raise ValueError(f'{patronymic} is not a valid ru patronymic')
        return patronymic

    @validates('country')
    def validate_country(self, key, country):
        if not StringValidator.is_cyrillic_plus(country):
            raise ValueError(f'{country} is not a valid ru country')
        return country

    @validates('email')
    def validate_email(self, key, email):
        if not StringValidator.is_valid_email(email):
            raise ValueError(f'{email} is not a valid email')
        return email
