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
