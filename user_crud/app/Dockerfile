FROM python:3.11.1-buster

WORKDIR /usr/src/user_crud/app

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/user_crud/app/requirements.txt
COPY . /usr/src/user_crud/app/

RUN pip install -r /usr/src/user_crud/app/requirements.txt
