# Generated by Django 2.1.1 on 2020-07-31 12:09

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields
import djmoney.models.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inn', models.IntegerField(validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(999)], verbose_name='ИНН')),
                ('balance_currency', djmoney.models.fields.CurrencyField(choices=[('RUB', 'Russian Ruble')], default='XYZ', editable=False, max_length=3)),
                ('balance', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), max_digits=10, validators=[djmoney.models.validators.MinMoneyValidator(0)], verbose_name='Баланс счёта')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
    ]
