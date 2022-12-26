from celery import Celery
from flask import Flask

from settings import settings


app = Flask(__name__)
app.config.from_object(settings)
celery = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=['tasks']
)
celery.conf.timezone = 'UTC'
