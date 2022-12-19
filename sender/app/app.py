from flask import Flask

from settings import settings


app = Flask(__name__)
app.config.from_object(settings)

