FROM python:3.11.1-buster

WORKDIR /usr/src/social/tests

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/social/tests/requirements.txt
COPY . /usr/src/social/tests/

RUN pip install -r /usr/src/social/tests/requirements.txt
