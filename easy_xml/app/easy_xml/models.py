from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, help_text='Название продукта')

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return self.name


class Tariff(models.Model):
    name = models.CharField(max_length=255, help_text='Название тарифа')
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text='Стоимость',
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text='Продукт')

    class Meta:
        ordering = ['name', '-price']

    def __str__(self):
        return self.name


class Promotion(models.Model):
    name = models.CharField(max_length=255, help_text='Название акции')
    discount = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text='Процент скидки',
        db_index=True,
    )
    start_at = models.DateField(help_text='Дата начала акции')
    end_at = models.DateField(help_text='Дата завершения акции')
    tariffs = models.ManyToManyField(Tariff)

    class Meta:
        ordering = ['name', '-discount']

    def __str__(self):
        return self.name
