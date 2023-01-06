import json
import jwt

from flask import jsonify, request
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from peewee import OperationalError

from app import app
from auth_middleware import token_required
from logger import logger
from models import (db, Person, Apartment, Booking)
from settings import settings
from validators import (
    LoginModel, CreatePersonModel, UpdatePersonModel, ApartmentModel,
    BookingModel, ResponseSuccessModel, ResponseFailureModel
)


PREFIX = f'api/v{settings.API_VERSION}'

api = FlaskPydanticSpec('flask')


@app.route(f'/{PREFIX}/login', methods=['POST'])
@api.validate(
    body=Request(LoginModel),
    resp=Response(
        HTTP_200=ResponseSuccessModel,
        HTTP_404=ResponseFailureModel,
        HTTP_500=ResponseFailureModel,
    ),
    tags=['person']
)
def login():
    try:
        body = request.get_json()
        username = body['username']
        password = body['password']
        person = Person.login(username, password)
        if person:
            try:
                # token should expire after 24 hours
                token = jwt.encode(
                    {'username': person.username},
                    settings.SECRET_KEY,
                    algorithm='HS256'
                )
                data = ResponseSuccessModel(
                    error=False,
                    error_message=None,
                    success_message=f'Person {person.id} logged in',
                    data={'token': token}
                )
                return jsonify(json.loads(data.json())), 200
    
            except Exception as e:
                logger.error(str(e))
                data = ResponseFailureModel(
                    error=True,
                    error_message='JWT encode error',
                    success_message=None
                )
                return jsonify(json.loads(data.json())), 500

        data = ResponseFailureModel(
            error=True,
            error_message='Invalid username or password',
            success_message=None
        )
        return jsonify(json.loads(data.json())), 404

    except Exception as e:
        data = ResponseFailureModel(
            error=True,
            error_message='Login failure',
            success_message=None
        )
        return jsonify(json.loads(data.json())), 500


@app.route(f'/{PREFIX}/person', methods=['POST'])
@token_required
@api.validate(
    body=Request(CreatePersonModel),
    resp=Response(HTTP_200=ResponseSuccessModel, HTTP_500=ResponseFailureModel),
    tags=['person']
)
def add_person():

    body = request.get_json()
    first_name = body['first_name']
    second_name = body['second_name']
    username = body['username']
    password = body['password']

    with db.atomic() as tx:
        try:
            person = Person(
                first_name=first_name, second_name=second_name, username=username
            )
            person.set_password(password)
            person.save()
    
        except Exception as e:
            logger.error(str(e))
            tx.rollback()
            data = ResponseFailureModel(
                error=True,
                error_message='Create person failure',
                success_message=None
            )
            return jsonify(json.loads(data.json())), 500
        
        tx.commit()
        data = ResponseSuccessModel(
            error=False,
            error_message=None,
            success_message=f'Person {person.id} created'
        )
        return jsonify(json.loads(data.json())), 200


@app.route(f'/{PREFIX}/person/<int:person_id>', methods=['PUT'])
@token_required
@api.validate(
    body=Request(UpdatePersonModel),
    resp=Response(
        HTTP_200=ResponseSuccessModel,
        HTTP_400=ResponseFailureModel,
        HTTP_404=ResponseFailureModel,
        HTTP_500=ResponseFailureModel
    ),
    tags=['person']
)
def update_person(person_id: int):

    with db.atomic() as tx:
        try:
            person = Person.get_or_none(Person.id==person_id)
            if person is None:
                data = ResponseFailureModel(
                    error=True,
                    error_message=f'Person {person_id} not found',
                    success_message=None,
                    data={}
                )
                return jsonify(json.loads(data.json())), 404

            body = request.get_json()
            first_name = body.get('first_name')
            second_name = body.get('second_name')
            username = body.get('username')
            password = body.get('password')
            
            if first_name:
                person.first_name = first_name
            if second_name:
                person.second_name = second_name
            if username:
                person.username = username
            if password:
                person.set_password(password)

            person.save()

            error_data = ResponseFailureModel(
                error=True,
                error_message='Update person failure',
                success_message=None
            )

        except OperationalError as e:
            logger.error(str(e))           
            tx.rollback()
            return jsonify(json.loads(error_data.json())), 500
        except Exception as e:
            logger.error(str(e))
            tx.rollback()
            return jsonify(json.loads(error_data.json())), 400

        tx.commit()
        data = ResponseSuccessModel(
            error=False,
            error_message=None,
            success_message=f'Person {person_id} updated'
        )
        return jsonify(json.loads(data.json())), 200


@app.route(f'/{PREFIX}/person/<int:person_id>', methods=['DELETE'])
@token_required
@api.validate(
    resp=Response(
        HTTP_200=ResponseSuccessModel,
        HTTP_404=ResponseFailureModel,
        HTTP_500=ResponseFailureModel
    ),
    tags=['person']
)
def delete_person(person_id: int):

    with db.atomic() as tx:
        try:
            person = Person.get_or_none(Person.id==person_id)
            if person is None:
                data = ResponseFailureModel(
                    error=True,
                    error_message=f'Person {person_id} not found',
                    success_message=None
                )
                return jsonify(json.loads(data.json())), 404

            person.delete_instance()

            error_data = ResponseFailureModel(
                error=True,
                error_message='Delete person failure',
                success_message=None
            )

        except OperationalError as e:
            logger.error(str(e))
            tx.rollback()
            return jsonify(json.loads(error_data.json())), 500
        except Exception as e:
            logger.error(str(e))
            tx.rollback()
            return jsonify(json.loads(error_data.json())), 400
        
        tx.commit()
        data = ResponseSuccessModel(
            error=False,
            error_message=None,
            success_message=f'Person {person_id} deleted'
        )
        return jsonify(json.loads(data.json())), 200


@app.route(f'/{PREFIX}/apartment', methods=['POST'])
@token_required
@api.validate(
    body=Request(ApartmentModel),
    resp=Response(HTTP_200=ResponseSuccessModel, HTTP_500=ResponseFailureModel),
    tags=['apartment']
)
def add_apartment():

    body = request.get_json()
    room_number = body['room_number']

    try:
        apartment_id = Apartment.insert(room_number=room_number).execute()
    except Exception as e: 
        logger.error(str(e))
        data = ResponseFailureModel(
            error=True,
            error_message='Create apartment failure',
            success_message=None
        )
        return jsonify(json.loads(data.json())), 500

    data = ResponseSuccessModel(
        error=False,
        error_message=None,
        success_message=f'Apartment {apartment_id} created'
    )
    return jsonify(json.loads(data.json())), 200


@app.route(f'/{PREFIX}/apartment/<int:apartment_id>', methods=['PUT'])
@token_required
@api.validate(
    body=Request(ApartmentModel),
    resp=Response(
        HTTP_200=ResponseSuccessModel,
        HTTP_400=ResponseFailureModel,
        HTTP_404=ResponseFailureModel,
        HTTP_500=ResponseFailureModel
    ),
    tags=['apartment']
)
def update_apartment(apartment_id: int):

    with db.atomic() as tx:
        try:
            apartment = Apartment.get_or_none(Apartment.id==apartment_id)
            if apartment is None:
                data = ResponseFailureModel(
                    error=True,
                    error_message=f'Apartment {apartment_id} not found',
                    success_message=None
                )
                return jsonify(json.loads(data.json())), 404

            body = request.get_json()
            room_number = body['room_number']
            Apartment.update(room_number=room_number).where(
                Apartment.id==apartment_id
            ).execute()

            error_data = ResponseFailureModel(
                error=True,
                error_message='Update apartment failure',
                success_message=None
            )

        except OperationalError as e:
            tx.rollback()
            logger.error(str(e))
            return jsonify(json.loads(error_data.json())), 500
        except Exception as e:
            tx.rollback()
            logger.error(str(e))
            return jsonify(json.loads(error_data.json())), 400

        tx.commit()
        data = ResponseSuccessModel(
            error=False,
            error_message=None,
            success_message=f'Apartment {apartment_id} updated'
        )
        return jsonify(json.loads(data.json())), 200


@app.route(f'/{PREFIX}/apartment/<int:apartment_id>', methods=['DELETE'])
@token_required
@api.validate(
    resp=Response(
        HTTP_200=ResponseSuccessModel,
        HTTP_404=ResponseFailureModel,
        HTTP_500=ResponseFailureModel
    ),
    tags=['apartment']
)
def delete_apartment(apartment_id: int):

    with db.atomic() as tx:
        try:
            apartment = Apartment.get_or_none(Apartment.id==apartment_id)
            if apartment is None:
                data = ResponseFailureModel(
                    error=True,
                    error_message=f'Apartment {apartment_id} not found',
                    success_message=None
                )
                return jsonify(json.loads(data.json())), 404

            apartment.delete_instance()
        
        except Exception as e:
            tx.rollback()
            logger.error(str(e))
            error_data = ResponseFailureModel(
                error=True,
                error_message='Delete apartment failure',
                success_message=None
            )
            return jsonify(json.loads(error_data.json())), 500

        tx.commit()

        data = ResponseSuccessModel(
            error=False,
            error_message=None,
            success_message=f'Apartment {apartment_id} deleted'
        )
        return jsonify(json.loads(data.json())), 200


# create booking
# update booking
# delete booking

# docker
# tests

if __name__ == '__main__':
    api.register(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
