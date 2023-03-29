import decimal

from django.db import transaction
from django.db.models import F
from djmoney.money import Money

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import PaymentUser
from .serializers import PaymentUserSerializer


class MoneySender(APIView):
    """
    Отправка суммы с баланса пользователя другим пользователям.
    """
    def post(self, request, inn):
        serializer = PaymentUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_404_NOT_FOUND
            )

        sender = PaymentUser.objects.filter(inn=inn).first()
        if sender is None:
            return Response(
                'Отправитель не найден', status=status.HTTP_404_NOT_FOUND
            )

        send_sum = serializer.validated_data['send_sum']
        if serializer.validated_data['send_sum'] > sender.balance.amount:
            return Response(
                'Недостаточно средств на балансе пользователя',
                status=status.HTTP_400_BAD_REQUEST
            )

        recipients = serializer.validated_data['recipients']
        valid_recipient_count = PaymentUser.objects.filter(
            inn__in=recipients
        ).count()
        if valid_recipient_count != len(recipients):
            return Response(
                'Обнаружены некорректные получатели',
                status=status.HTTP_400_BAD_REQUEST
            )

        send_sum_each = send_sum / len(recipients)
        send_sum_each_money = Money(
            decimal.Decimal(
                str(send_sum_each)).quantize(
                    decimal.Decimal('.01'),
                    rounding=decimal.ROUND_DOWN
            ),
            currency='RUB'
        )
        withdraw_sum = send_sum_each_money * len(recipients)
        with transaction.atomic():
            sender.balance = F('balance') - withdraw_sum
            sender.save()
            recipient_objs = PaymentUser.objects.filter(
                inn__in=recipients
            )
            for recipient in recipient_objs:
                recipient.balance = F('balance') + send_sum_each_money
            PaymentUser.objects.bulk_update(recipient_objs, ['balance'])

        return Response(status=status.HTTP_201_CREATED)
