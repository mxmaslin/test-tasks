import json

from flask import jsonify
from flask_pydantic import validate
from peewee import fn

from app import app
from logger import logger
from models import (
    db, Mailing, Recipient, MailingRecipient, Tag, TagRecipient, Message,
    MessageMailing
)
from settings import settings
from validators import RequestRecipientModel, ResponseModel, RequestMailingModel


PREFIX = f'api/v{settings.API_VERSION}'


@app.route(f'/{PREFIX}/recipient', methods=['POST'])
@validate()
def add_recipient(body: RequestRecipientModel):
    with db.atomic() as tx:
        try:
            phone_number = body.phone_number
            op_code = body.op_code
            tz = body.tz
            recipient_id = Recipient.insert(
                phone_number=phone_number, op_code=op_code, tz=tz
            ).execute()
    
            tags = body.tags
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
            data = ResponseModel(
                error=True,
                error_message='Create recipient failure',
                success_message=None
            )
            return jsonify(json.loads(data.json())), 400

        tx.commit()
        data = ResponseModel(
            error=False,
            error_message=None,
            success_message=f'Recipient {recipient_id} created'
        )
        return jsonify(json.loads(data.json())), 200



@app.route(f'/{PREFIX}/recipients/<int:recipient_id>', methods=['PUT'])
@validate()
def update_recipient(recipient_id: int, body: RequestRecipientModel):
    with db.atomic() as tx:
        try:
            phone_number = body.phone_number
            op_code = body.op_code
            tz = body.tz
            Recipient.update(
                phone_number=phone_number, op_code=op_code, tz=tz
            ).where(Recipient.id==recipient_id).execute()
    
            tags = body.tags
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
            data = ResponseModel(
                error=True,
                error_message='Update recipient failure',
                success_message=None
            )
            return jsonify(json.loads(data.json())), 400

        tx.commit()
        data = ResponseModel(
            error=False,
            error_message=None,
            success_message=f'Recipient {recipient_id} updated'
        )
        return jsonify(json.loads(data.json())), 200



@app.route(f'/{PREFIX}/recipients/<int:recipient_id>', methods=['DELETE'])
@validate()
def delete_recipient(recipient_id: int):
    with db.atomic() as tx:
        try:
            recipient = Recipient.get(Recipient.id==recipient_id)
            recipient.delete_instance(recursive=True)

        except Exception as e:
            tx.rollback()
            logger.error(str(e))
            data = ResponseModel(
                error=True,
                error_message='Delete recipient failure',
                success_message=None
            )
            return jsonify(json.loads(data.json())), 400

        tx.commit()
        data = ResponseModel(
            error=False,
            error_message=None,
            success_message=f'Recipient {recipient_id} deleted'
        )
        return jsonify(json.loads(data.json())), 200


@app.route(f'/{PREFIX}/mailing', methods=['POST'])
@validate()
def add_mailing(body: RequestMailingModel):
    with db.atomic() as tx:
        try:
            start = body.start
            end = body.end
            mailing_id = Mailing.insert(start=start, end=end).execute()

            # мы не хотим
            # 1. создавать Messages для Recipients, которых нет в бд
            # 2. создавать Messages по одному
            # для этого нам надо сформировать список Recipients из запроса,
            # отобрав те из них, которые есть в бд
            # проблема в том, что в запросе к нам прилетают не id реципиентов,
            # а их телефонные номера (я так захотел).
            # Вот как я решил эту проблему:
            messages = [x.dict() for x in body.messages]
            recipient_phone_numbers = {
                x['recipient_phone_number'] for x in messages
            }
            recipients = Recipient.select().where(
                Recipient.phone_number.in_(recipient_phone_numbers)
            ).order_by(Recipient.phone_number).execute()
            recipients = {x.phone_number: x.id for x in recipients}
            messages = {x['recipient_phone_number']: x for x in messages}
            messages_to_create = []
            for k, v in recipients.items():
                message = messages[k]
                message['recipient_id'] = v
                messages_to_create.append(message)
            messages_to_create = [
                Message(
                    status=0,
                    value=x['value'],
                    recipient_id=x['recipient_id']
                )
                for x in messages_to_create
            ]
            Message.bulk_create(messages_to_create)

            recipient_ids = [
                v['recipient_id']
                for _, v in messages.items() if v.get('recipient_id')
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

        except Exception as e:
            tx.rollback()
            logger.error(str(e))
            data = ResponseModel(
                error=True,
                error_message='Create mailing failure',
                success_message=None
            )
            return jsonify(json.loads(data.json())), 400

        tx.commit()
        data = ResponseModel(
            error=False,
            error_message=None,
            success_message=f'Mailing {mailing_id} created'
        )
        return jsonify(json.loads(data.json())), 200


@app.route(f'/{PREFIX}/mailing', methods=['GET'])
@validate()
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
    data = ResponseModel(
        error=False,
        error_message=None,
        success_message=f'Mailings stat success',
        data=mailings_data
    )
    return jsonify(json.loads(data.json())), 200


@app.route(f'/{PREFIX}/mailings/<int:mailing_id>', methods=['GET'])
@validate()
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
    data = ResponseModel(
        error=False,
        error_message=None,
        success_message=f'Mailing stat success',
        data=mailing_data
    )
    return jsonify(json.loads(data.json())), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
