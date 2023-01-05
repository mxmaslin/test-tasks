import json

from flask import jsonify, request
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request

from app import app
from models import (db, Person, Apartment, Booking)
from settings import settings
from validators import (
    UserModel, ApartmentModel, BookingModel, ResponseModel, ResponseSuccessModel, ResponseFailureModel
)


PREFIX = f'api/v{settings.API_VERSION}'

api = FlaskPydanticSpec('flask')


@app.route(f'/{PREFIX}/person', methods=['POST'])
@api.validate(
    body=Request(UserModel),
    resp=Response(HTTP_200=ResponseSuccessModel, HTTP_400=ResponseFailureModel),
    tags=['person']
)
def add_person():

    body = request.get_json()
    first_name = body['first_name']
    second_name = body['second_name']
    username = body['username']
    password = body['password']
    password_hash = Person.set_password(password)

    try:
        person_id = Person.insert(
            first_name=first_name,
            second_name=second_name,
            username=username,
            password_hash=password_hash
        ).execute()
    except Exception as e: 
        logger.error(str(e))
        data = ResponseFailureModel(
            error=True,
            error_message='Create person failure',
            success_message=None
        )
        return jsonify(json.loads(data.json())), 400

    data = ResponseSuccessModel(
        error=False,
        error_message=None,
        success_message=f'Recipient {person_id} created'
    )
    return jsonify(json.loads(data.json())), 200


# create person
# update person
# delete person

# create apartment
# update apartment
# delete apartment

# create booking
# update booking
# delete booking