# Objective

Create web-application for online reservations.

# Completion levels

Each level includes previous levels.

## Level 1

Only BE, allows at least basic CRUD operations, tests.

## Level 2

More comprehensive db schema, more complex validation, thorough tests, well-documented readme, required tooling is included or can be deployed easily on local machine.

## Level 3

Includes FE part (any of SPA, PWA, MPA), uses advanced tooling, hosted is a plus but not a must.

# Implementation notes

Перед запуском проекта, переименуйте `.env.local` в `.env` и задайте переменные для используемой бд. 

Для запуска проекта выполните команду `docker-compose up`.

Для запуска юнит-тестов выполните команду `pytest test_booking.py`.

Документация реализована при помощи [flask-pydantic-spec](https://github.com/turner-townsend/flask-pydantic-spec) и доступна по адресу `/apidoc/swagger`.
