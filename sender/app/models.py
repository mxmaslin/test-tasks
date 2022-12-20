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
            (('start',), False),
            (('end',), False),
            (('start', 'end'), False),
        )

    def __repr__(self):
        return f'Mailing(id={self.id},start={self.start},end={self.end})'


class Recipient(BaseModel):
    phone_number = CharField(max_length=30)
    op_code = CharField(max_length=30, null=True)
    tz = CharField(max_length=255, null=True)

    class Meta:
        indexes = (
            (('phone_number',), True),
        )


class Tag(BaseModel):
    value = TextField()

    class Meta:
        indexes = (
            (('value',), False),
        )


class Message(BaseModel):
    STATUS_CHOICES = (
        (0, 'Scheduled'),
        (1, 'Sent'),
    )
    sent_at = DateTimeField(null=True)
    status = IntegerField(choices=STATUS_CHOICES, default=0)
    value = TextField()
    recipient = ForeignKeyField(Recipient)

    class Meta:
        indexes = (
            (('sent_at',), False),
            (('recipient',), False),
            (('sent_at', 'status'), False),
        )


class MailingRecipient(BaseModel):
    mailing = ForeignKeyField(Mailing)
    recipient = ForeignKeyField(Recipient)

    class Meta:
        indexes = (
            (('mailing', 'recipient'), True),
        )


class MessageMailing(BaseModel):
    message = ForeignKeyField(Message)
    mailing = ForeignKeyField(Mailing)

    class Meta:
        indexes = (
            (('message', 'mailing'), True),
        )


class TagRecipient(BaseModel):
    tag = ForeignKeyField(Tag)
    recipient = ForeignKeyField(Recipient)

    class Meta:
        indexes = (
            (('tag', 'recipient'), True),
        )
