import json

from functools import wraps

import jwt

from flask import request, jsonify, current_app

from logger import logger
from models import Person
from validators import ResponseFailureModel


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        if not token:
            logger.error('Token is absent in headers')
            data = ResponseFailureModel(
                error=True,
                error_message='Auth token missing',
                success_message=None
            )
            return jsonify(json.loads(data.json())), 401

        try:
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms=['HS256']
            )
            current_user = Person.get(Person.id == data['user_id'])
            if current_user is None:
                data = ResponseFailureModel(
                    error=True,
                    error_message='Invalid auth token',
                    success_message=None
                )
                return jsonify(json.loads(data.json())), 401

        except Exception as e:
            logger.error(str(e))
            data = ResponseFailureModel(
                error=True,
                error_message='Something went wrong',
                success_message=None
            )
            return jsonify(json.loads(data.json())), 500

        return f(current_user, *args, **kwargs)

    return decorated
