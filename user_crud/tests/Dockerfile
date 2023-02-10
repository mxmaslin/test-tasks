# FROM python:3.11.1-buster
FROM ubuntu:latest

WORKDIR /usr/src/social/tests

RUN set -xe \
    && apt-get update -y \
    && apt-get install python3-pip sqlite3 libsqlite3-dev -y 

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/social/tests/requirements.txt
COPY . /usr/src/social/tests/
RUN pip install -r /usr/src/social/tests/requirements.txt

# COPY ./init_test_db.sql ./usr/src/social/tests/init_test_db.sql
# RUN cd ./system_init/db/ && sqlite3 database.db < init_db.sql

# RUN /usr/bin/sqlite3 /db/test.db
# CMD /bin/bash

RUN sqlite3 ./test.db < ./init_test_db.sql