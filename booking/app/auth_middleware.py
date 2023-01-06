from functools import wraps

import jwt

from flask import request, abort
from flask import current_app

from models import Person


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        if not token:
            payload = {
                'message': 'Auth token missing',
                'data': None,
                'error': 'Unauthorized'
            }
            return payload, 401
        try:
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms=['HS256']
            )
            current_user = Person.get(Person.id == data['user_id'])
            if current_user is None:
                payload = {
                    'message': 'Invalid Authentication token!',
                    'data': None,
                    'error': 'Unauthorized'
                }
                return payload, 401
            if not current_user['active']:
                abort(403)
        except Exception as e:
            payload = {
                'message': 'Something went wrong',
                'data': None,
                'error': str(e)
            }
            return payload, 500

        return f(current_user, *args, **kwargs)

    return decorated
