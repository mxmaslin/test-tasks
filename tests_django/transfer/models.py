from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from djmoney.models.fields import MoneyField



class Client(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')
    inn = models.IntegerField(
        validators=[MinValueValidator(100), MaxValueValidator(999)],
        verbose_name='ИНН')
    balance = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        verbose_name='Баланс счёта')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return str(self.inn)
