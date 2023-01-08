from functools import wraps

import pytest

from playhouse.sqlite_ext import SqliteExtDatabase

from api import app, PREFIX
from models import Booking, Person, Apartment


def with_test_db(func):
    @wraps(func)
    def test_db_closure(*args, **kwargs):
        test_db = SqliteExtDatabase(':memory:')
        models = (Booking, Person, Apartment)
        with test_db.bind_ctx(models):
            test_db.create_tables(models)
            test_db.execute_sql('''
                INSERT INTO person VALUES (1, 'John', 'Doe', 'johndoe1', 'pbkdf2:sha256:260000$MsAdIe40HIsCBN5J$da412dd99a87b86b2adfc39d406bd63a0fd86bbaa2958fd40001dfe4da745ec8'),
                    (2, 'John', 'Doe', 'johndoe2', 'pbkdf2:sha256:260000$eqXwWOxYEK4adx4f$c8c42b7dfc308793b0a0353aaa60f97402b462cfcfdac6a1c591fa0e7ce892d0');
            ''')
            test_db.execute_sql('INSERT INTO apartment VALUES (1, 100);')
            test_db.execute_sql("INSERT INTO booking VALUES (1, '2023-01-01', '2024-01-01', 1, 2);")
            try:
                return func(*args, **kwargs)
            finally:
                test_db.drop_tables(models)
                test_db.close()

    return test_db_closure


@pytest.fixture
@with_test_db
def token():
    with app.test_client() as test_client:
        person = Person.select().first()
        response = test_client.post(
            f'{PREFIX}/login',
            json={'username': person.username, 'password': 'password'}
        )
        return 'Bearer ' + response.get_json()['data']['token']


@with_test_db
def test_create_person():
    with app.test_client() as test_client:
        data = {
            'first_name': 'John',
            'second_name': 'Doe',
            'username': 'johndoe3',
            'password': 'password'
        }
        response = test_client.post(f'{PREFIX}/person', json=data)
        assert response.status_code == 200
        assert 'result' in response.get_json()['data']


@with_test_db
def test_update_person(token):
    with app.test_client() as test_client:
        person = Person.select().first()
        data = {
            'first_name': 'John',
            'second_name': 'Doe',
            'username': 'johndoe4',
            'password': 'password'
        }
        response = test_client.put(
            f'{PREFIX}/person/{person.id}',
            json=data,
            headers={'Authorization': token}
        )
        assert response.status_code == 200
        assert 'result' in response.get_json()['data']


@with_test_db
def test_delete_person(token):
    with app.test_client() as test_client:
        person = Person.select().first()
        response = test_client.delete(
            f'{PREFIX}/person/{person.id}',
            headers={'Authorization': token}
        )
        assert response.status_code == 200


@with_test_db
def test_create_apartment(token):
    with app.test_client() as test_client:
        data = {'room_number': 777}
        response = test_client.post(
            f'{PREFIX}/apartment',
            json=data,
            headers={'Authorization': token}
        )
        assert response.status_code == 200
        assert 'result' in response.get_json()['data']


@with_test_db
def test_update_apartment(token):
    with app.test_client() as test_client:
        apartment = Apartment.select().first()
        data = {'room_number': 666}
        response = test_client.put(
            f'{PREFIX}/apartment/{apartment.id}',
            json=data,
            headers={'Authorization': token}
        )
        assert response.status_code == 200
        assert response.get_json()['data']['result'] == data['room_number']


@with_test_db
def test_delete_apartment(token):
    with app.test_client() as test_client:
        apartment = Apartment.select().first()
        response = test_client.delete(
            f'{PREFIX}/apartment/{apartment.id}',
            headers={'Authorization': token}
        )
        assert response.status_code == 200


@with_test_db
def test_create_booking(token):
    with app.test_client() as test_client:
        apartment = Apartment.select().first()
        person_ids = [p.id for p in Person.select().execute()]
        data = {
            'start_date': '2023-1-1',
            'end_date': '2024-1-1',
            'person_ids': person_ids,
            'apartment_id': apartment.id
        }
        response = test_client.post(
            f'{PREFIX}/booking',
            json=data,
            headers={'Authorization': token}
        )
        assert response.status_code == 200
        assert 'result' in response.get_json()['data']
        assert len(person_ids) == len(response.get_json()['data']['result'])


@with_test_db
def test_update_booking(token):
    with app.test_client() as test_client:
        booking = Booking.select().first()
        person = Person.select().first()
        apartment = Apartment.select().first()
        data = {
            'start_date': '2024-1-1',
            'end_date': '2025-1-1',
            'person_id': person.id,
            'apartment_id': apartment.id
        }
        response = test_client.put(
            f'{PREFIX}/booking/{booking.id}',
            json=data,
            headers={'Authorization': token}
        )
        assert response.status_code == 200
        assert 'result' in response.get_json()['data']


@with_test_db
def test_delete_booking(token):
    with app.test_client() as test_client:
        booking = Booking.select().first()
        response = test_client.delete(
            f'{PREFIX}/booking/{booking.id}',
            headers={'Authorization': token}
        )
        assert response.status_code == 200
