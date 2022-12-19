from flask import Flask, request, jsonify
from flask_pydantic import validate

from app import app
from logger import logger
from models import (
    db, Mailing, Recipient, MailingRecipient, Tag, TagRecipient, Message,
    MessageMailing
)
from settings import settings
from validators import RequestRecipientModel


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
                TagRecipient(tag=tag, recipient=recipient.id)
                for tag in db_tags_ids
            ]
            TagRecipient.bulk_create(tag_recipients)
        except Exception as e:
            tx.rollback()
            logger.error(str(e))
            return str(e), 400

        tx.commit()
        return 'Success', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
