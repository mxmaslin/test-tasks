from celery import Celery
from flask import Flask

from settings import settings


app = Flask(__name__)
app.config.from_object(settings)
celery = Celery(
    __name__,
    # broker='amqp://guest@localhost//',
    broker=settings.BROKER_URL,
    backend=settings.RESULT_BACKEND,
    include=['tasks']
)
celery.conf.timezone = 'UTC'
