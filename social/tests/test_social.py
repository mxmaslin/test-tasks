import os

from functools import wraps

import pytest

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.storage import User, Post, Like, Dislike
from tests.mocks import redis, test_database


def with_test_db(func):
    @wraps(func)
    def test_db_closure(*args, **kwargs):
        models = User, Post, Like, Dislike
        with test_database.bind_ctx(models):
            test_database.create_tables(models)
            try:
                return func(*args, **kwargs)
            finally:
                test_database.drop_tables(models)
                test_database.close()

    return test_db_closure


@with_test_db
@pytest.fixture(scope='session')
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


@with_test_db
def test_signup(client):
    data = {'email': 'project777@mail.ru', 'password': 'test'}
    response = client.post('/signup', json=data)
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'User 1 created'


@with_test_db
def test_signup_not_unique(client):
    data = {'email': 'project777@mail.ru', 'password': 'test'}
    client.post('/signup', json=data)
    response = client.post('/signup', json=data)
    assert response.status_code == 500


@with_test_db
def test_get_token(client):
    data = {'email': 'project777@mail.ru', 'password': 'test'}
    client.post('/signup', json=data)
    response = client.post('/token', json=data)
    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data


@with_test_db
def test_get_token_invalid_user(client):
    data = {'email': 'wrong@mail.ru', 'password': 'test'}
    response = client.post('/token', json=data)
    data = response.json()
    assert data['detail'] == 'Incorrect username or password'


@with_test_db
def test_create_post(client):
    data = {'email': 'project777@mail.ru', 'password': 'test'}
    client.post('/signup', json=data)
    response = client.post('/token', json=data)
    data = response.json()
    token = data['access_token']

    data = {'title': 'post title', 'content': 'post content'}
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/posts', json=data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Post 1 created'


@with_test_db
def test_update_post(client):
    data = {'email': 'project777@mail.ru', 'password': 'test'}
    client.post('/signup', json=data)
    response = client.post('/token', json=data)
    data = response.json()
    token = data['access_token']

    data = {'title': 'post title', 'content': 'post content'}
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/posts', json=data, headers=headers)
    data = response.json()
    _, post_id, _ = data['message'].split()

    data = {'title': 'updated post title', 'content': 'updated post content'}
    response = client.put(f'/posts/{post_id}', json=data, headers=headers)

    data = response.json()
    assert response.status_code == 200
    assert data['message'] == 'Post 1 updated'


@with_test_db
def test_delete_post(client):
    data = {'email': 'project777@mail.ru', 'password': 'test'}
    client.post('/signup', json=data)
    response = client.post('/token', json=data)
    data = response.json()
    token = data['access_token']

    data = {'title': 'post title', 'content': 'post content'}
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/posts', json=data, headers=headers)
    data = response.json()
    _, post_id, _ = data['message'].split()

    response = client.delete(f'/posts/{post_id}', headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Post 1 deleted'


@with_test_db
def test_like_own_post(client):
    data = {'email': 'project777@mail.ru', 'password': 'test'}
    client.post('/signup', json=data)
    response = client.post('/token', json=data)
    data = response.json()
    token = data['access_token']

    data = {'title': 'post title', 'content': 'post content'}
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/posts', json=data, headers=headers)
    data = response.json()
    _, post_id, _ = data['message'].split()

    response = client.post(f'/posts/{post_id}/like', headers=headers)
    data = response.json()
    assert data['status_code'] == 400
    assert data['detail'] == 'Unable to like own post'


@with_test_db
@patch('app.storage.get_redis', new=redis)
def test_like_others_post(client):
    # create UserA and get a token for the UserA
    data_a = {'email': 'project777@mail.ru', 'password': 'test'}
    client.post('/signup', json=data_a)
    response = client.post('/token', json=data_a)
    data = response.json()
    token_a = data['access_token']

    # create post by userA
    data_a_post = {'title': 'post title', 'content': 'post content'}
    headers_a = {'Authorization': f'Bearer {token_a}'}
    response = client.post('/posts', json=data_a_post, headers=headers_a)
    data = response.json()
    _, post_id, _ = data['message'].split()

    # create UserB and get a token for the UserB
    data_b = {'email': 'project888@gmail.com', 'password': 'test'}
    client.post('/signup', json=data_b)
    response = client.post('/token', json=data_b)
    data = response.json()
    token_b = data['access_token']

    # like UserA post by UserB
    headers_b = {'Authorization': f'Bearer {token_b}'}
    response = client.post(f'/posts/{post_id}/like', headers=headers_b)
    data = response.json()
    print('2', data)
    # assert data['detail'] == 'Unable to like own post'
