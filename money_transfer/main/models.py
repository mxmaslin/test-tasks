from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator


class PaymentUser(User):
    inn_validator = RegexValidator(
        regex=r'^[0-9]{10}$',
        message='ИНН должен содержать в точности 10 цифр'
    )

    inn = models.CharField(
        max_length=10,
        unique=True,
        validators=[inn_validator],
        verbose_name='ИНН',
    )

    balance = MoneyField(
        max_digits=14,
        decimal_places=2,
        default=0,
        default_currency='RUB',
        validators=[MinMoneyValidator(0)],
    )

    class Meta:
        indexes = [
            models.Index(fields=['inn'], name='inn_idx')
        ]
