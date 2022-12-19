from flask import Flask, request, jsonify
from flask_pydantic import validate
from flask_restful import Api, Resource

from app import app
from models import (
    Mailing, Recipient, MailingRecipient, Tag, TagRecipient, Message,
    MessageMailing
)
from settings import settings
from validators import RequestRecipientModel


PREFIX = f'api/v{settings.API_VERSION}'


@app.route(f'/{PREFIX}/recipient', methods=['POST'])
@validate()
def add_recipient(body: RequestRecipientModel):
    return 'Helloa!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)