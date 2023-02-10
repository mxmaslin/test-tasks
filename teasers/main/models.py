from django.db import models
from django.contrib.auth.models import User

from djmoney.models.fields import MoneyField


class Teaser(models.Model):
    header = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    category = models.CharField()
    status = models.CharField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Payment(models.Model):
    payment_sum = MoneyField(
        max_digits=14, decimal_places=2, default_currency='RUB'
    )
    teaser = models.OneToOneField(Teaser, on_delete=models.CASCADE)


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
