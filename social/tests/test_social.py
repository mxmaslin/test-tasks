import os

from functools import wraps

import pytest

from unittest import mock

from fastapi.testclient import TestClient
from peewee_async import PostgresqlDatabase

import app
from app.main import app
from app.settings import settings
from app.storage import User, Post, Like, Dislike


@mock.patch.dict(os.environ, {'POSTGRES_DB': 'test_social'})
def with_test_db(func):
    @wraps(func)
    def test_db_closure(*args, **kwargs):
        test_database = PostgresqlDatabase(
            os.getenv('POSTGRES_DB'),
            host=settings().POSTGRES_HOST,
            port=settings().POSTGRES_PORT,
            user=settings().POSTGRES_USER,
            password=settings().POSTGRES_PASSWORD
        )

        models = User, Post, Like, Dislike
        with test_database.bind_ctx(models):
            test_database.create_tables(models)
            try:
                return func(*args, **kwargs)
            finally:
                test_database.drop_tables(models)
                test_database.close()

    return test_db_closure


@pytest.fixture(scope='session')
def client() -> TestClient:
    with TestClient(app) as c:
        yield c



# @pytest.fixture
# def token(client):
#     data = {'email': 'project777@mail.ru', 'password': 'test'}
#     response = client.post('/token', json=data)
#     print(response)


@with_test_db
def test_signup(client):
    data = {'email': 'project777@mail.ru', 'password': 'test'}
    response = client.post('/signup', json=data)
    assert response.status_code == 200


# @with_test_db
# def test_signup_not_unique(client):
#     data = {'email': 'project777@mail.ru', 'password': 'test'}
#     client.post('/signup', json=data)
#     response = client.post('/signup', json=data)
#     assert response.status_code == 500


@with_test_db
def test_get_token(client):
    data = {'email': 'project777@mail.ru', 'password': 'test'}
    client.post('/signup', json=data)