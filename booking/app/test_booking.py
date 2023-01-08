from functools import wraps

import pytest

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from playhouse.sqlite_ext import SqliteExtDatabase

from api import app, PREFIX
from models import Person


def with_test_db():
    def decorator(func):
        @wraps(func)
        def test_db_closure(*args, **kwargs):
            test_db = SqliteExtDatabase(':memory:')
            models = (Person,)
            with test_db.bind_ctx(models):
                test_db.create_tables(models)
                test_db.execute_sql(
                    '''INSERT INTO person VALUES (1, 'John', 'Doe', 'johndoe1', 'pbkdf2:sha256:260000$MsAdIe40HIsCBN5J$da412dd99a87b86b2adfc39d406bd63a0fd86bbaa2958fd40001dfe4da745ec8'),
                    (2, 'John', 'Doe', 'johndoe2', 'pbkdf2:sha256:260000$eqXwWOxYEK4adx4f$c8c42b7dfc308793b0a0353aaa60f97402b462cfcfdac6a1c591fa0e7ce892d0');
                    '''
                )
                try:
                    func(*args, **kwargs)
                finally:
                    test_db.drop_tables(models)
                    test_db.close()

        return test_db_closure

    return decorator


@with_test_db()
def test_create_person():
    with app.test_client() as test_client:
        data = {
            'first_name': 'John',
            'second_name': 'Doe',
            'username': 'vovovo',
            'password': 'password'
        }
        response = test_client.post(f'{PREFIX}/person', json=data)
        assert response.status_code == 200
        assert 'result' in response.get_json()['data']
