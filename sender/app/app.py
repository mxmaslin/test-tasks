from flask import Flask
from flask_restful import Api

from settings import settings


app = Flask(__name__)
app.config.from_object(settings)

