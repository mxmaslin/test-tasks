import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.dependencies import get_db, get_redis
from tests.dependencies import get_redis_mock, override_get_db, test_db

app.dependency_overrides[get_redis] = get_redis_mock
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope='session')
def client() -> TestClient:
    client = TestClient(app)
    with client as c:
        yield c


def test_signup(client, test_db):
    data = {'email': 'project777@mail.ru', 'password': 'test'}
    response = client.post('/signup', json=data)
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'User 1 created'


def test_signup_not_unique(client, test_db):
    data = {'email': 'project777@mail.ru', 'password': 'test'}
    client.post('/signup', json=data)
    response = client.post('/signup', json=data)
    assert response.status_code == 500


def test_get_token(client, test_db):
    data = {'email': 'project777@mail.ru', 'password': 'test'}
    client.post('/signup', json=data)
    response = client.post('/token', json=data)
    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data


def test_get_token_invalid_user(client, test_db):
    data = {'email': 'wrong@mail.ru', 'password': 'test'}
    response = client.post('/token', json=data)
    data = response.json()
    assert data['detail'] == 'Incorrect username or password'


def test_create_post(client, test_db):
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


def test_update_post(client, test_db):
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


def test_delete_post(client, test_db):
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


def test_like_own_post(client, test_db):
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


def test_like_others_post(client, test_db):
    # create UserA and get a token for the UserA
    data_a = {'email': 'project777@mail.ru', 'password': 'test'}
    client.post('/signup', json=data_a)
    response = client.post('/token', json=data_a)
    data = response.json()
    token_a = data['access_token']

    # create post by userA
    post_data = {'title': 'post title', 'content': 'post content'}
    headers_a = {'Authorization': f'Bearer {token_a}'}
    response = client.post('/posts', json=post_data, headers=headers_a)
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
    assert response.status_code == 200


def test_dislike_own_post(client, test_db):
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

    response = client.post(f'/posts/{post_id}/dislike', headers=headers)
    data = response.json()
    assert data['status_code'] == 400
    assert data['detail'] == 'Unable to dislike own post'


def test_dislike_others_post(client, test_db):
    # create UserA and get a token for the UserA
    data_a = {'email': 'project777@mail.ru', 'password': 'test'}
    client.post('/signup', json=data_a)
    response = client.post('/token', json=data_a)
    data = response.json()
    token_a = data['access_token']

    # create post by userA
    post_data = {'title': 'post title', 'content': 'post content'}
    headers_a = {'Authorization': f'Bearer {token_a}'}
    response = client.post('/posts', json=post_data, headers=headers_a)
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
    response = client.post(f'/posts/{post_id}/dislike', headers=headers_b)
    assert response.status_code == 200
