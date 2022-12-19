import json

from flask import jsonify
from flask_pydantic import validate

from app import app
from logger import logger
from models import (
    db, Mailing, Recipient, MailingRecipient, Tag, TagRecipient, Message,
    MessageMailing
)
from settings import settings
from validators import RequestRecipientModel, ResponseRecipientModel


PREFIX = f'api/v{settings.API_VERSION}'


@app.route(f'/{PREFIX}/recipient', methods=['POST'])
@validate()
def add_recipient(body: RequestRecipientModel):
    with db.atomic() as tx:
        try:
            phone_number = body.phone_number
            op_code = body.op_code
            tz = body.tz
            recipient = Recipient(phone_number=phone_number, op_code=op_code, tz=tz)
            recipient.save()
    
            tags = body.tags
            db_tags = [Tag(value=tag) for tag in tags]
            Tag.bulk_create(db_tags)

            db_tags_ids = [tag.id for tag in db_tags]
            tag_recipients = [
                TagRecipient(tag=tag_id, recipient=recipient.id)
                for tag_id in db_tags_ids
            ]
            TagRecipient.bulk_create(tag_recipients)
        except Exception as e:
            tx.rollback()
            logger.error(str(e))
            data = ResponseRecipientModel(
                error=True,
                error_message=str(e),
                success_message=None
            )
            return jsonify(json.loads(data.json())), 400

        tx.commit()
        data = ResponseRecipientModel(
            error=False,
            error_message=None,
            success_message=f'Recipient {recipient.id} created'
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
            query = Recipient.update(
                phone_number=phone_number, op_code=op_code, tz=tz
            ).where(Recipient.id==recipient_id)
            query.execute()
    
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
            data = ResponseRecipientModel(
                error=True,
                error_message=str(e),
                success_message=None
            )
            return jsonify(json.loads(data.json())), 400

        tx.commit()
        data = ResponseRecipientModel(
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

            print('yay', r)
    
        except Exception as e:
            tx.rollback()
            logger.error(str(e))
            data = ResponseRecipientModel(
                error=True,
                error_message=str(e),
                success_message=None
            )
            return jsonify(json.loads(data.json())), 400

        tx.commit()
        data = ResponseRecipientModel(
            error=False,
            error_message=None,
            success_message=f'Recipient {recipient_id} deleted'
        )
        return jsonify(json.loads(data.json())), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
