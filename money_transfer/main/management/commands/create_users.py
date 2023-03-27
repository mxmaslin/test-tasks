from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from main.models import PaymentUser


class Command(BaseCommand):
    help = 'Создаёт три пользователя с балансом 1000 у каждого'

    def handle(self, *args, **options):

        inns = ['1234567890', '1234567891', '1234567892']

        for inn in inns:
            user = PaymentUser.objects.create_user(
                username=inn,
                inn=inn,
                balance=1000
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Пользователь {user.username} успешно создан'
                )
            )
