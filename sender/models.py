from peewee import *


db = PostgresqlDatabase('sender')


class BaseModel(Model):
    class Meta:
        database = db


class Mailing(BaseModel):
    start = DateTimeField()
    end = DateTimeField()

    class Meta:
        indexes = (
            (('start',), True),
            (('end',), True),
            (('start', 'end'), True),
        )


class Recipient(BaseModel):
    phone_number = CharField(max_length=11)
    op_code = CharField(max_length=3)
    tz = CharField(max_length=9)

    class Meta:
        indexes = (
            (('phone_number',), True),
        )

class MailingRecipient(BaseModel):
    mailing = ForeignKeyField(Mailing)
    recipient = ForeignKeyField(Recipient)

    class Meta:
        indexes = (
            (('mailing', 'recipient'), True),
        )


class Tag(BaseModel):
    value = TextField()

    class Meta:
        indexes = (
            (('value',), True),
        )


class TagRecipient(BaseModel):
    tag = ForeignKeyField(Tag)
    recipient = ForeignKeyField(Recipient)

    class Meta:
        indexes = (
            (('tag', 'recipient'), True),
        )


class Message(BaseModel):
    STATUS_CHOICES = (
        (0, 'Scheduled'),
        (1, 'Sent'),
    )
    sent_at = DateTimeField()
    status = IntegerField(choices=STATUS_CHOICES, default=0)
    value = TextField()
    recipient = ForeignKeyField(Recipient)

    class Meta:
        indexes = (
            (('sent_at',), True),
            (('recipient',), True),
            (('sent_at', 'status'), True),
        )


class MessageMailing(BaseModel):
    message = ForeignKeyField(Message)
    mailing = ForeignKeyField(Mailing)

    class Meta:
        indexes = (
            (('message', 'mailing'), True),
        )