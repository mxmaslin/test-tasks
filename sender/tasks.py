import requests

from datetime import datetime

from celery.schedules import crontab

from app import celery
from logger import logger
from models import Message
from settings import settings


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(10.0, periodic_send_messages.s(), name='start every 10 seconds')

    sender.add_periodic_task(
        crontab(hour=1, minute=1),
        periodic_send_messages.s(),
    )


@celery.task
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
    messages_to_update = Message.select().where(Message.id.in_(messages_to_update_ids))
    for message in messages_to_update:
        message.status = 1
        message.sent_at = datetime.now()
    Message.bulk_update(messages_to_update, fields=[Message.status, Message.sent_at])


@celery.task
def periodic_send_messages():
    pass