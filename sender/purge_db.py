from app.models import (
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


if __name__ == '__main__':
    main()
