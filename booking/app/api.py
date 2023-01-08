import json

from datetime import timedelta

from flask import jsonify, request
from flask_jwt_extended import jwt_required, create_access_token
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from peewee import OperationalError

from app import app
from logger import logger
from models import (db, Person, Apartment, Booking)
from settings import settings
from validators import (
    LoginModel, CreatePersonModel, UpdatePersonModel, ApartmentModel,
    BookingModel, UpdateBookingModel, ResponseSuccessModel, ResponseFailureModel
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
                jwt_token = create_access_token(
                    (username, password), expires_delta=timedelta(hours=24)
                )
                data = ResponseSuccessModel(
                    error=False,
                    error_message=None,
                    success_message=f'Person {person.id} logged in',
                    data={'token': jwt_token}
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
            success_message=f'Person {person.id} created',
            data={'result': person.id}
        )
        return jsonify(json.loads(data.json())), 200


@app.route(f'/{PREFIX}/person/<int:person_id>', methods=['PUT'])
@jwt_required()
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

        except OperationalError as e:
            logger.error(str(e))           
            tx.rollback()
            error_data = ResponseFailureModel(
                error=True,
                error_message='Update person db failure',
                success_message=None
            )
            return jsonify(json.loads(error_data.json())), 500
        except Exception as e:
            logger.error(str(e))
            tx.rollback()
            error_data = ResponseFailureModel(
                error=True,
                error_message='Update person client failure',
                success_message=None
            )
            return jsonify(json.loads(error_data.json())), 400

        tx.commit()
        data = ResponseSuccessModel(
            error=False,
            error_message=None,
            success_message=f'Person {person_id} updated'
        )
        return jsonify(json.loads(data.json())), 200


@app.route(f'/{PREFIX}/person/<int:person_id>', methods=['DELETE'])
@jwt_required()
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

            person.delete_instance(recursive=True)

        except OperationalError as e:
            logger.error(str(e))
            tx.rollback()
            error_data = ResponseFailureModel(
                error=True,
                error_message='Delete person db failure',
                success_message=None
            )
            return jsonify(json.loads(error_data.json())), 500
        except Exception as e:
            logger.error(str(e))
            tx.rollback()
            error_data = ResponseFailureModel(
                error=True,
                error_message='Delete person client failure',
                success_message=None
            )
            return jsonify(json.loads(error_data.json())), 400
        
        tx.commit()
        data = ResponseSuccessModel(
            error=False,
            error_message=None,
            success_message=f'Person {person_id} deleted'
        )
        return jsonify(json.loads(data.json())), 200


@app.route(f'/{PREFIX}/apartment', methods=['POST'])
@jwt_required()
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
@jwt_required()
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

        except OperationalError as e:
            tx.rollback()
            logger.error(str(e))
            error_data = ResponseFailureModel(
                error=True,
                error_message='Update apartment db failure',
                success_message=None
            )
            return jsonify(json.loads(error_data.json())), 500
        except Exception as e:
            tx.rollback()
            logger.error(str(e))
            error_data = ResponseFailureModel(
                error=True,
                error_message='Update apartment client failure',
                success_message=None
            )
            return jsonify(json.loads(error_data.json())), 400

        tx.commit()
        data = ResponseSuccessModel(
            error=False,
            error_message=None,
            success_message=f'Apartment {apartment_id} updated'
        )
        return jsonify(json.loads(data.json())), 200


@app.route(f'/{PREFIX}/apartment/<int:apartment_id>', methods=['DELETE'])
@jwt_required()
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


@app.route(f'/{PREFIX}/booking', methods=['POST'])
@jwt_required()
@api.validate(
    body=Request(BookingModel),
    resp=Response(HTTP_200=ResponseSuccessModel, HTTP_500=ResponseFailureModel),
    tags=['booking']
)
def add_booking():

    body = request.get_json()
    start_date = body['start_date']
    end_date = body['end_date']
    person_ids = body['person_ids']
    apartment_id = body['apartment_id']

    with db.atomic() as tx:
        try:
            apartment = Apartment.get_by_id(apartment_id)
            persons = Person.select().where(Person.id.in_(person_ids))
            data = [
                {
                    'start_date': start_date,
                    'end_date': end_date,
                    'apartment': apartment,
                    'person': p,
                }
                for p in persons
            ]
            bookings = Booking.insert_many(data)
            booking_ids = ', '.join([str(b[0]) for b in bookings])
    
        except Exception as e:
            logger.error(str(e))
            tx.rollback()
            data = ResponseFailureModel(
                error=True,
                error_message='Create booking db failure',
                success_message=None
            )
            return jsonify(json.loads(data.json())), 500
        
        tx.commit()
        data = ResponseSuccessModel(
            error=False,
            error_message=None,
            success_message=f'Bookings {booking_ids} created'
        )
        return jsonify(json.loads(data.json())), 200


@app.route(f'/{PREFIX}/booking/<int:booking_id>', methods=['PUT'])
@jwt_required()
@api.validate(
    body=Request(UpdateBookingModel),
    resp=Response(HTTP_200=ResponseSuccessModel, HTTP_500=ResponseFailureModel),
    tags=['booking']
)
def update_booking(booking_id):

    with db.atomic() as tx:
        try:
            booking = Booking.get_or_none(Booking.id == booking_id)
            if booking is None:
                data = ResponseFailureModel(
                    error=True,
                    error_message=f'Booking {booking_id} not found',
                    success_message=None,
                    data={}
                )
                return jsonify(json.loads(data.json())), 404

            body = request.get_json()
            start_date = body['start_date']
            end_date = body['end_date']
            person_id = body['person_id']
            apartment_id = body['apartment_id']

            if start_date:
                booking.start_date = start_date
            if end_date:
                booking.end_date = end_date
            if person_id:
                booking.person_id = person_id
            if apartment_id:
                booking.apartment_id = apartment_id
            
            booking.save()
    
        except Exception as e:
            logger.error(str(e))
            tx.rollback()
            data = ResponseFailureModel(
                error=True,
                error_message='Create booking db failure',
                success_message=None
            )
            return jsonify(json.loads(data.json())), 500
        
        tx.commit()
        data = ResponseSuccessModel(
            error=False,
            error_message=None,
            success_message=f'Booking {booking_id} updated'
        )
        return jsonify(json.loads(data.json())), 200


@app.route(f'/{PREFIX}/booking/<int:booking_id>', methods=['DELETE'])
@jwt_required()
@api.validate(
    resp=Response(
        HTTP_200=ResponseSuccessModel,
        HTTP_404=ResponseFailureModel,
        HTTP_500=ResponseFailureModel
    ),
    tags=['booking']
)
def delete_booking(booking_id: int):

    with db.atomic() as tx:
        try:
            booking = Booking.get_or_none(Booking.id == booking_id)
            if booking is None:
                data = ResponseFailureModel(
                    error=True,
                    error_message=f'Booking {booking_id} not found',
                    success_message=None
                )
                return jsonify(json.loads(data.json())), 404

            booking.delete_instance()
        
        except Exception as e:
            tx.rollback()
            logger.error(str(e))
            error_data = ResponseFailureModel(
                error=True,
                error_message='Delete booking db failure',
                success_message=None
            )
            return jsonify(json.loads(error_data.json())), 500

        tx.commit()

        data = ResponseSuccessModel(
            error=False,
            error_message=None,
            success_message=f'Booking {booking_id} deleted'
        )
        return jsonify(json.loads(data.json())), 200


# tests
# resource


if __name__ == '__main__':
    api.register(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
