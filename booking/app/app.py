from flask import Flask

from flask_jwt_extended import JWTManager

from settings import settings


app = Flask(__name__)
app.config.from_object(settings)
JWTManager(app)
