from django.test import TestCase

from .forms import SendMoneyForm
from .models import Client


class SendMoneyFormTestCase(TestCase):
    fixtures = ['testdata', 'auth', 'contenttypes']

    def test_valid_recipient(self):
        form_data = {
            'donor': '3',
            'recipients': '101',
            'amount_0': '3',
            'amount_1': 'RUB'}
        form = SendMoneyForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_recipients(self):
        form_data = {
            'donor': '3',
            'recipients': '101 100',
            'amount_0': '3',
            'amount_1': 'RUB'}
        form = SendMoneyForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_recipient_absent(self):
        form_data = {
            'donor': '3',
            'recipients': '101 109',
            'amount_0': '3',
            'amount_1': 'RUB'}
        form = SendMoneyForm(data=form_data)
        self.assertIn(
            'Инн 109 отсутствует в базе данных', form.errors['recipients'])

    def test_invalid_sum_negative(self):
        form_data = {
            'donor': '3',
            'recipients': '101 100',
            'amount_0': '-1',
            'amount_1': 'RUB'}
        form = SendMoneyForm(data=form_data)
        self.assertIn(
            'Это поле не может быть меньше 0.01', form.errors['amount'])

    def test_invalid_sum_larger(self):
        form_data = {
            'donor': '3',
            'recipients': '101 100',
            'amount_0': '1000000',
            'amount_1': 'RUB'}
        form = SendMoneyForm(data=form_data)
        self.assertIn(
            'Сумма превышает баланс отправителя', form.errors['amount'])
