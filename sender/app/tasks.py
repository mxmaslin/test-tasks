import requests

from datetime import datetime

from celery.utils.log import get_task_logger

from app import celery
from models import db, Mailing, MailingRecipient, Message, MessageMailing, Recipient
from settings import settings


logger = get_task_logger(__name__)

HOUR = 3600


celery.conf.beat_schedule = {
    'every-hour': {
        'task': 'tasks.periodic_send_messages',
        'schedule': HOUR
    }
}


def get_periodic_messages_to_send() -> list:
    now = datetime.now()
    entries = Mailing.select(Message.id, Message.value, Recipient.phone_number) \
        .join(MailingRecipient) \
        .join(Recipient).switch(Mailing) \
        .join(MessageMailing) \
        .join(Message) \
        .where(
            now >= Mailing.start, now <= Mailing.end,
            Message.status == 0 
        ).objects()
    messages_to_send = [
        {'message_id': x.id, 'phone': x.phone_number, 'text': x.value}
        for x in entries
    ]
    return messages_to_send


def send_messages(messages_to_send: list):
    auth_token = settings.SENDER_TOKEN
    headers = {'Authorization': 'Bearer ' + auth_token, 'Content-Type': 'application/json'}
    messages_to_update_ids = []
    for message_to_send in messages_to_send:
        url = f'{settings.SENDER_URL}/{message_to_send["message_id"]}'
        json = {
            'id': message_to_send['message_id'],
            'phone': message_to_send['phone'],
            'text': message_to_send['text']
        }
        response = requests.post(url, json=json, headers=headers)
        if response.status_code == 200:
            message_to_update_id = message_to_send['message_id']
            messages_to_update_ids.append(message_to_update_id)
        else:
            logger.warning(f'Failed to send message {message_to_send["message_id"]}')
    messages_to_update = Message.select().where(
        Message.id.in_(messages_to_update_ids)
    )
    for message in messages_to_update:
        message.status = 1
        message.sent_at = datetime.now()
    if messages_to_update.count() > 0:
        with db.atomic() as tx:
            try:
                Message.bulk_update(messages_to_update, fields=[Message.status, Message.sent_at])
            except:
                tx.rollback()
            else:
                tx.commit()



@celery.task
def send_messages_delayed(messages_to_send: list) -> None:
    send_messages(messages_to_send)


@celery.task
def periodic_send_messages() -> None:
    messages_to_send = get_periodic_messages_to_send()
    send_messages(messages_to_send)
