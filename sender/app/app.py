from celery import Celery
from flask import Flask

from settings import settings


app = Flask(__name__)
app.config.from_object(settings)
app.config.update(CELERY_CONFIG={
    'broker_url': settings.BROKER_URL,
    'result_backend': settings.RESULT_BACKEND
})


def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config['CELERY_CONFIG'])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)
