from flask import Flask

from flask_jwt_extended import JWTManager
from flask_pydantic_spec import FlaskPydanticSpec

from settings import settings


app = Flask(__name__)
app.config.from_object(settings)
JWTManager(app)
api = FlaskPydanticSpec('flask')
