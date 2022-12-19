from flask import Flask, request, jsonify
from flask_restful import Api, Resource

from app import app
from settings import settings
from models import (
    Mailing, Recipient, MailingRecipient, Tag, TagRecipient, Message,
    MessageMailing
)


PREFIX = f'api/v{settings.API_VERSION}'


@app.route(f'/{PREFIX}/recipient', methods=['POST'])
def add_recipient():
    query = Mailing.select()
    for r in query:
        print(r.end)
    return 'Helloa!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)