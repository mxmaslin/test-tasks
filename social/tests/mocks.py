from peewee_async import PostgresqlDatabase
from pytest_mock_resources import create_redis_fixture


test_database = PostgresqlDatabase(
    'test_social',
    host='localhost',
    port=5432,
    user='social',
    password='test'
)

redis = create_redis_fixture()
