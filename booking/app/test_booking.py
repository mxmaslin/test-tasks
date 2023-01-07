from functools import wraps

from playhouse.sqlite_ext import SqliteExtDatabase


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


@with_test_db
def test_something():
    pass
