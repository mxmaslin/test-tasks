FROM python:3.11.1-buster

WORKDIR /usr/src/social/app

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/social/app/requirements.txt
COPY . /usr/src/social/app/

RUN pip install -r /usr/src/social/app/requirements.txt
