from functools import wraps

from playhouse.sqlite_ext import SqliteExtDatabase

from tasks import get_periodic_messages_to_send


def with_test_db(func):
    @wraps(func)
    def test_db_closure(*args, **kwargs):
        test_db = SqliteExtDatabase(':memory:')
        models = ()
        with test_db.bind_ctx(models):
            test_db.create_tables(models)
            test_db.execute_sql()
            try:
                return func(*args, **kwargs)
            finally:
                test_db.drop_tables(models)
                test_db.close()

    return test_db_closure


def test_get_periodic_messages_to_send():
    pass
