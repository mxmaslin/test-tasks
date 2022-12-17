from flask import request, jsonify

from app import app
from models import (
    Mailing, Recipient, MailingRecipient, Tag, TagRecipient, Message,
    MessageMailing
)


@app.route('/')
def hello():
    query = Mailing.select()
    for r in query:
        print(r.end)
    return 'Helloa!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)