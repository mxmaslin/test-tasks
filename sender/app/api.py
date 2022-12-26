import json
import pytz
import requests

from datetime import datetime
from flask import jsonify, request
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from peewee import fn

from app import app
from logger import logger
from models import (
    db, Mailing, Recipient, MailingRecipient, Tag, TagRecipient, Message,
    MessageMailing
)
from settings import settings
from tasks import send_messages
from validators import (
    RequestRecipientModel, RequestMailingModel, ResponseSuccessModel,
    ResponseFailureModel, SenderDataModel
)


PREFIX = f'api/v{settings.API_VERSION}'

api = FlaskPydanticSpec('flask')


def get_messages_to_send(messages_enriched: list, messages_to_create: list):
    messages_to_send = []
    for message_enriched, message_to_create in zip(
        messages_enriched, messages_to_create
    ):
        message_to_send = {
            'message_id': message_to_create.id,
            'phone': message_enriched['recipient_phone_number'],
            'text': message_enriched['value'],
            'recipient_id': message_to_create.recipient.id
        }
        messages_to_send.append(message_to_send)
    return messages_to_send


def send_message(id_: int, data: SenderDataModel):
    url = f'{settings.SENDER_URL}/{id_}'
    auth_token = settings.SENDER_TOKEN
    headers = {'Authorization': 'Bearer ' + auth_token, 'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    return response


@app.route(f'/{PREFIX}/recipient', methods=['POST'])
@api.validate(
    body=Request(RequestRecipientModel),
    resp=Response(HTTP_200=ResponseSuccessModel, HTTP_400=ResponseFailureModel),
    tags=['recipient']
)
def add_recipient():

    body = request.get_json()
    phone_number = body['phone_number']
    op_code = body['op_code']
    tz = body['tz']

    with db.atomic() as tx:
        try:
            recipient_id = Recipient.insert(
                phone_number=phone_number, op_code=op_code, tz=tz
            ).execute()
    
            tags = body['tags']
            db_tags = [Tag(value=tag) for tag in tags]
            Tag.bulk_create(db_tags)

            db_tags_ids = [tag.id for tag in db_tags]
            tag_recipients = [
                TagRecipient(tag=tag_id, recipient=recipient_id)
                for tag_id in db_tags_ids
            ]
            TagRecipient.bulk_create(tag_recipients)

        except Exception as e:
            tx.rollback()
            logger.error(str(e))
            data = ResponseFailureModel(
                error=True,
                error_message='Create recipient failure',
                success_message=None
            )
            return jsonify(json.loads(data.json())), 400

        tx.commit()
        data = ResponseSuccessModel(
            error=False,
            error_message=None,
            success_message=f'Recipient {recipient_id} created'
        )
        return jsonify(json.loads(data.json())), 200


@app.route(f'/{PREFIX}/recipient/<int:recipient_id>', methods=['PUT'])
@api.validate(
    body=Request(RequestRecipientModel),
    resp=Response(
        HTTP_200=ResponseSuccessModel,
        HTTP_400=ResponseFailureModel,
        HTTP_404=ResponseFailureModel
    ),
    tags=['recipient']
)
def update_recipient(recipient_id: int):

    body = request.get_json()
    phone_number = body['phone_number']
    op_code = body['op_code']
    tz = body['tz']

    with db.atomic() as tx:
        try:
            recipient = Recipient.get_or_none(Recipient.id==recipient_id)
            if recipient is None:
                data = ResponseFailureModel(
                    error=True,
                    error_message=f'Recipient {recipient_id} not found',
                    success_message=None,
                    data=[]
                )
                return jsonify(json.loads(data.json())), 404

            Recipient.update(
                phone_number=phone_number, op_code=op_code, tz=tz
            ).where(Recipient.id==recipient_id).execute()
    
            tags = body['tags']
            tag_recipients = TagRecipient.select().join(Tag).where(
                TagRecipient.recipient==recipient_id,
                Tag.value.in_(tags)

            ).execute()
            tags_to_create = list(
                set(tags) - {x.tag.value for x in tag_recipients}
            )
            tags_to_create = [Tag(value=tag) for tag in tags_to_create]
            Tag.bulk_create(tags_to_create)

            tags_to_create_ids = [tag.id for tag in tags_to_create]
            tag_recipients = [
                TagRecipient(tag=tag_id, recipient=recipient_id)
                for tag_id in tags_to_create_ids
            ]
            TagRecipient.bulk_create(tag_recipients)

        except Exception as e:
            tx.rollback()
            logger.error(str(e))
            data = ResponseFailureModel(
                error=True,
                error_message='Update recipient failure',
                success_message=None
            )
            return jsonify(json.loads(data.json())), 400

        tx.commit()
        data = ResponseSuccessModel(
            error=False,
            error_message=None,
            success_message=f'Recipient {recipient_id} updated'
        )
        return jsonify(json.loads(data.json())), 200


@app.route(f'/{PREFIX}/recipient/<int:recipient_id>', methods=['DELETE'])
@api.validate(
    resp=Response(
        HTTP_200=ResponseSuccessModel,
        HTTP_404=ResponseFailureModel
    ),
    tags=['recipient']
)
def delete_recipient(recipient_id: int):

    recipient = Recipient.get_or_none(Recipient.id==recipient_id)
    if recipient is None:
        data = ResponseFailureModel(
            error=True,
            error_message=f'Recipient {recipient_id} not found',
            success_message=None,
            data=[]
        )
        return jsonify(json.loads(data.json())), 404

    recipient.delete_instance(recursive=True)

    data = ResponseSuccessModel(
        error=False,
        error_message=None,
        success_message=f'Recipient {recipient_id} deleted',
        data=[]
    )
    return jsonify(json.loads(data.json())), 200


@app.route(f'/{PREFIX}/mailing', methods=['POST'])
@api.validate(
    body=Request(RequestMailingModel),
    resp=Response(HTTP_200=ResponseSuccessModel, HTTP_400=ResponseFailureModel),
    tags=['mailing']
)
def add_mailing():

    body = request.get_json()
    start = body['start']
    end = body['end']
    messages = body['messages']

    with db.atomic() as tx:
        try:
            mailing_id = Mailing.insert(start=start, end=end).execute()

            # мы не хотим
            # 1. создавать Messages для Recipients, которых нет в бд
            # 2. создавать Messages по одному
            # для этого нам надо сформировать список Recipients из клиентского запроса,
            # отобрав те из них, которые есть в бд
            # проблема в том, что в запросе к нам прилетают не id реципиентов,
            # а их телефонные номера (я так захотел).
            # Вот как я решил эту проблему:
            recipient_phone_numbers = {
                x['recipient_phone_number'] for x in messages
            }
            recipients = Recipient.select().where(
                Recipient.phone_number.in_(recipient_phone_numbers)
            ).execute()
            recipients = {x.phone_number: x.id for x in recipients}
            messages_annotated = {x['recipient_phone_number']: x for x in messages}
            messages_enriched = []
            for k, v in recipients.items():
                message = messages_annotated[k]
                message['recipient_id'] = v
                messages_enriched.append(message)
            messages_to_create = [
                Message(
                    status=0,
                    value=x['value'],
                    recipient_id=x['recipient_id']
                )
                for x in messages_enriched
            ]
            Message.bulk_create(messages_to_create)

            recipient_ids = [
                v['recipient_id']
                for _, v in messages_annotated.items() if v.get('recipient_id')
            ]
            mailing_recipient = [
                MailingRecipient(mailing=mailing_id, recipient=recipient_id)
                for recipient_id in recipient_ids
            ]
            MailingRecipient.bulk_create(mailing_recipient)

            message_ids = [x.id for x in messages_to_create]
            message_mailing = [
                MessageMailing(mailing=mailing_id, message=message_id)
                for message_id in message_ids
            ]
            MessageMailing.bulk_create(message_mailing)

            now = datetime.now(pytz.utc)
            start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S.%f%z')
            end = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S.%f%z')
            if start <= now <= end:
                messages_to_send = get_messages_to_send(
                    messages_enriched, messages_to_create
                )
                send_messages.delay(messages_to_send)

        except Exception as e:
            tx.rollback()
            logger.error(str(e))
            data = ResponseFailureModel(
                error=True,
                error_message='Create mailing failure',
                success_message=None
            )
            return jsonify(json.loads(data.json())), 400

        tx.commit()
        data = ResponseSuccessModel(
            error=False,
            error_message=None,
            success_message=f'Mailing {mailing_id} created'
        )
        return jsonify(json.loads(data.json())), 200


@app.route(f'/{PREFIX}/mailing', methods=['GET'])
@api.validate(
    resp=Response(HTTP_200=ResponseSuccessModel),
    tags=['mailing']
)
def get_mailings_stat():

    mailings = Mailing.select(
        Mailing.id,
        Mailing.start,
        Mailing.end,
        fn.COUNT(Message.id).alias('messages_count')
    ).join(MessageMailing).join(Message).group_by(
        Mailing.id, Message.status
    ).execute()
    mailings_data = [
        {
            'start': x.start.strftime('%Y-%m-%d, %H:%M:%S'),
            'end': x.end.strftime('%Y-%m-%d, %H:%M:%S'),
            'messages_count': x.messages_count
        }
        for x in mailings
    ]
    data = ResponseSuccessModel(
        error=False,
        error_message=None,
        success_message=f'Mailings stat success',
        data=mailings_data
    )
    from tasks import periodic_send_messages
    periodic_send_messages()
    return jsonify(json.loads(data.json())), 200


@app.route(f'/{PREFIX}/mailing/<int:mailing_id>', methods=['GET'])
@api.validate(
    resp=Response(
        HTTP_200=ResponseSuccessModel,
        HTTP_400=ResponseFailureModel,
        HTTP_404=ResponseFailureModel
    ),
    tags=['mailing']
)
def get_mailing_stat(mailing_id: int):

    mailing = Mailing.select(
        Mailing.id,
        Mailing.start,
        Mailing.end,
        fn.COUNT(Message.id).alias('messages_count')
    ).join(MessageMailing).join(Message).group_by(
        Mailing.id, Message.status
    ).where(Mailing.id==mailing_id).execute()
    mailing_data = [
        {
            'start': x.start.strftime('%Y-%m-%d, %H:%M:%S'),
            'end': x.end.strftime('%Y-%m-%d, %H:%M:%S'),
            'messages_count': x.messages_count
        }
        for x in mailing
    ]
    if not mailing_data:
        data = ResponseFailureModel(
            error=True,
            error_message=f'Mailing {mailing_id} not found',
            success_message=None,
            data=[]
        )
        return jsonify(json.loads(data.json())), 404

    data = ResponseSuccessModel(
        error=False,
        error_message=None,
        success_message=f'Mailing {mailing_id} stat success',
        data=mailing_data
    )
    return jsonify(json.loads(data.json())), 200


@app.route(f'/{PREFIX}/mailing/<int:mailing_id>', methods=['PUT'])
@api.validate(
    body=Request(RequestMailingModel),
    resp=Response(
        HTTP_200=ResponseSuccessModel,
        HTTP_400=ResponseFailureModel,
        HTTP_404=ResponseFailureModel
    ),
    tags=['mailing']
)
def update_mailing(mailing_id: int):

    body = request.get_json()
    start = body['start']
    end = body['end']
    messages = body['messages']

    with db.atomic() as tx:
        try:
            mailing = Mailing.get_or_none(Mailing.id==mailing_id)
            if mailing is None:
                data = ResponseFailureModel(
                    error=True,
                    error_message=f'Mailing {mailing_id} not found',
                    success_message=None,
                    data=[]
                )
                return jsonify(json.loads(data.json())), 404

            mailing.update(start=start, end=end).execute()

            MailingRecipient.delete().where(MailingRecipient.mailing==mailing_id).execute()
            MessageMailing.delete().where(MessageMailing.mailing==mailing_id).execute()

            recipient_phone_numbers = {
                x['recipient_phone_number'] for x in messages
            }
            recipients = Recipient.select().where(
                Recipient.phone_number.in_(recipient_phone_numbers)
            ).execute()
            recipients = {x.phone_number: x.id for x in recipients}
            messages_annotated = {x['recipient_phone_number']: x for x in messages}
            messages_enriched = []
            for k, v in recipients.items():
                message = messages_annotated[k]
                message['recipient_id'] = v
                messages_enriched.append(message)
            messages_to_create = [
                Message(
                    status=0,
                    value=x['value'],
                    recipient_id=x['recipient_id']
                )
                for x in messages_enriched
            ]
            Message.bulk_create(messages_to_create)

            recipient_ids = [
                v['recipient_id']
                for _, v in messages_annotated.items() if v.get('recipient_id')
            ]
            mailing_recipient = [
                MailingRecipient(mailing=mailing_id, recipient=recipient_id)
                for recipient_id in recipient_ids
            ]
            MailingRecipient.bulk_create(mailing_recipient)

            message_ids = [x.id for x in messages_to_create]
            message_mailing = [
                MessageMailing(mailing=mailing_id, message=message_id)
                for message_id in message_ids
            ]
            MessageMailing.bulk_create(message_mailing)

            now = datetime.now(pytz.utc)
            start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S.%f%z')
            end = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S.%f%z')
            if start <=now <= end:
                messages_to_send = get_messages_to_send(
                    messages_enriched, messages_to_create
                )
                send_messages.delay(messages_to_send)            

        except Exception as e:
            tx.rollback()
            logger.error(str(e))
            data = ResponseFailureModel(
                error=True,
                error_message='Update mailing failure',
                success_message=None
            )
            return jsonify(json.loads(data.json())), 400

        tx.commit()
        data = ResponseSuccessModel(
            error=False,
            error_message=None,
            success_message=f'Mailing {mailing_id} updated'
        )
        return jsonify(json.loads(data.json())), 200


@app.route(f'/{PREFIX}/mailing/<int:mailing_id>', methods=['DELETE'])
@api.validate(
    resp=Response(HTTP_200=ResponseSuccessModel, HTTP_404=ResponseFailureModel),
    tags=['mailing']
)
def delete_mailing(mailing_id: int):

    mailing = Mailing.get_or_none(Mailing.id==mailing_id)
    if mailing is None:
        data = ResponseFailureModel(
            error=True,
            error_message=f'Mailing {mailing_id} not found',
            success_message=None,
            data=[]
        )
        return jsonify(json.loads(data.json())), 404

    mailing.delete_instance(recursive=True)

    data = ResponseSuccessModel(
        error=False,
        error_message=None,
        success_message=f'Mailing {mailing_id} deleted',
        data=[]
    )
    return jsonify(json.loads(data.json())), 200


if __name__ == '__main__':
    api.register(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
