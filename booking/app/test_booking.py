from functools import wraps

import pytest

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from playhouse.sqlite_ext import SqliteExtDatabase

from api import app, PREFIX
from models import Person




def with_test_db(models: tuple):
    def decorator(func):
        @wraps(func)
        def test_db_closure(*args, **kwargs):
            test_db = SqliteExtDatabase(':memory:')
            with test_db.bind_ctx(models):
                test_db.create_tables(models)
                try:
                    func(*args, **kwargs)
                finally:
                    test_db.drop_tables(models)
                    test_db.close()

        return test_db_closure

    return decorator


@with_test_db((Person,))
def test_something():
    with app.test_client() as test_client:
        data = {
            'first_name': 'John',
            'second_name': 'Doe',
            'username': 'johndoe',
            'password': 'password'
        }
        response = test_client.post(f'{PREFIX}/person', json=data)
        print('yay', response.get_json())
