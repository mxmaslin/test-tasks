import copy
import random

from datetime import timedelta

from faker import Faker

from models import (
    Mailing, Recipient, Tag, Message, MailingRecipient, TagRecipient,
    MessageMailing
)


def main():
    TagRecipient.delete().execute()
    MessageMailing.delete().execute()
    MailingRecipient.delete().execute()
    Mailing.delete().execute()
    Tag.delete().execute()
    Message.delete().execute()
    Recipient.delete().execute()

    num_mailings = num_messages = 10
    num_recipients = num_tags = 100

    fake = Faker()

    mailing_ids = []
    for _ in range(num_mailings):
        start = fake.date_time()
        end = start + timedelta(days=1)
        mailing = Mailing(start=start, end=end)
        mailing.save()
        mailing_ids.append(mailing.id)
    
    recipient_ids = []
    for _ in range(num_recipients):
        phone_number = '7' + fake.msisdn()[3:]
        op_code = fake.country_calling_code()
        tz = fake.timezone()
        recipient = Recipient(phone_number=phone_number, op_code=op_code, tz=tz)
        recipient.save()
        recipient_ids.append(recipient.id)

    tag_ids = []
    for _ in range(num_tags):
        value = fake.word()
        tag = Tag(value=value)
        tag.save()
        tag_ids.append(tag.id)

    message_ids = []
    num_sentences = 5
    for _ in range(num_messages):
        sent_at = fake.date_time()
        value = fake.paragraph(nb_sentences=num_sentences, variable_nb_sentences=True)

        statuses = '0000000011'
        status_position = random.randint(0, len(statuses)-1)
        status = statuses[status_position]
        
        recipient_position = random.randint(0, len(recipient_ids)-1)
        recipient_id = recipient_ids[recipient_position]
        
        message = Message(sent_at=sent_at, status=status, value=value, recipient=recipient_id)
        message.save()
        message_ids.append(message.id)

    mailing_ids2 = copy.copy(mailing_ids)
    for _ in range(num_mailings):
        mailing_position = random.randint(0, len(mailing_ids2)-1)
        mailing_id = mailing_ids2[mailing_position]
        mailing_ids2.remove(mailing_id)
        
        recipient_ids2 = copy.copy(recipient_ids)
        for _ in range(num_recipients):
            recipient_position = random.randint(0, len(recipient_ids2)-1)
            recipient_id = recipient_ids2[recipient_position]
            recipient_ids2.remove(recipient_id)
            MailingRecipient.insert(mailing=mailing_id, recipient=recipient_id).execute()


    tag_ids2 = copy.copy(tag_ids)
    for _ in range(num_tags):
        tag_position = random.randint(0, len(tag_ids2)-1)
        tag_id = tag_ids2[tag_position]
        tag_ids2.remove(tag_id)
        
        recipient_ids3 = copy.copy(recipient_ids)
        for _ in range(num_recipients):
            recipient_position = random.randint(0, len(recipient_ids3)-1)
            recipient_id = recipient_ids3[recipient_position]
            recipient_ids3.remove(recipient_id)
            TagRecipient.insert(tag=tag_id, recipient=recipient_id).execute()            

    message_ids2 = copy.copy(message_ids)
    for _ in range(num_messages):
        message_position = random.randint(0, len(message_ids2)-1)
        message_id = message_ids2[message_position]
        message_ids2.remove(message_id)
        
        mailing_ids3 = copy.copy(mailing_ids)
        for _ in range(num_mailings):
            mailing_position = random.randint(0, len(mailing_ids3)-1)
            mailing_id = mailing_ids3[mailing_position]
            mailing_ids3.remove(mailing_id)
            MessageMailing.insert(message=message_id, mailing=mailing_id).execute()


if __name__ == '__main__':
    main()
