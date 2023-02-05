from functools import wraps

from app.storage import User, Post, Like, Dislike

from tests.settings import settings


def with_test_db(func):
    @wraps(func)
    def test_db_closure(*args, **kwargs):
        models = User, Post, Like, Dislike
        test_database = PostgresqlDatabase(
            settings().TEST_POSTGRES_DB,
            host=settings().TEST_POSTGRES_HOST,
            port=settings().TEST_POSTGRES_PORT,
            user=settings().TEST_POSTGRES_USER,
            password=settings().TEST_POSTGRES_PASSWORD
        )
        with test_database.bind_ctx(models):
            test_database.create_tables(models)
            try:
                return func(*args, **kwargs)
            finally:
                test_database.drop_tables(models)
                test_database.close()

    return test_db_closure


class RedisMock:
    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)


def get_redis_mock():
    return RedisMock()
