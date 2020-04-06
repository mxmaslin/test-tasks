from django.test.client import Client as TestClient
from django.test import TestCase

from djmoney.money import Money

from .forms import SendMoneyForm
from .models import Client
from .views import SendMoneyFormView


class SendMoneyFormTestCase(TestCase):
    fixtures = ['transfer_money']

    def setUp(self):
        self.client = TestClient()

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

    def test_rounding_0_03_2(self):
        form_data = {
            'donor': '3',
            'recipients': '101 100',
            'amount_0': '0.03',
            'amount_1': 'RUB'}
        response = self.client.post(
            '/transfer-money/', form_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        donor = Client.objects.get(pk=3)
        recipient1 = Client.objects.get(pk=1)
        recipient2 = Client.objects.get(pk=2)
        expected_donor_balance = Money(9.98, 'RUB')
        expected_recipient1_balance = Money(10.01, 'RUB')
        expected_recipient2_balance = Money(10.01, 'RUB')
        self.assertEqual(donor.balance, expected_donor_balance)
        self.assertEqual(recipient1.balance, expected_recipient1_balance)
        self.assertEqual(recipient2.balance, expected_recipient2_balance)

    def test_rounding_0_03_3(self):
        form_data = {
            'donor': '3',
            'recipients': '101 100 102',
            'amount_0': '0.03',
            'amount_1': 'RUB'}
        response = self.client.post(
            '/transfer-money/', form_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        donor = Client.objects.get(pk=3)
        recipient1 = Client.objects.get(pk=1)
        recipient2 = Client.objects.get(pk=2)
        expected_donor_balance = Money(9.98, 'RUB')
        expected_recipient1_balance = Money(10.01, 'RUB')
        expected_recipient2_balance = Money(10.01, 'RUB')
        self.assertEqual(donor.balance, expected_donor_balance)
        self.assertEqual(recipient1.balance, expected_recipient1_balance)
        self.assertEqual(recipient2.balance, expected_recipient2_balance)

    def test_rounding_1_01_2(self):
        form_data = {
            'donor': '3',
            'recipients': '101 100',
            'amount_0': '1.01',
            'amount_1': 'RUB'}
        response = self.client.post(
            '/transfer-money/', form_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        donor = Client.objects.get(pk=3)
        recipient1 = Client.objects.get(pk=1)
        recipient2 = Client.objects.get(pk=2)
        expected_donor_balance = Money(9.00, 'RUB')
        expected_recipient1_balance = Money(10.50, 'RUB')
        expected_recipient2_balance = Money(10.50, 'RUB')
        self.assertEqual(donor.balance, expected_donor_balance)
        self.assertEqual(recipient1.balance, expected_recipient1_balance)
        self.assertEqual(recipient2.balance, expected_recipient2_balance)

    def test_even_transfer(self):
        form_data = {
            'donor': '3',
            'recipients': '101 100',
            'amount_0': '0.02',
            'amount_1': 'RUB'}
        response = self.client.post(
            '/transfer-money/', form_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        donor = Client.objects.get(pk=3)
        recipient1 = Client.objects.get(pk=1)
        recipient2 = Client.objects.get(pk=2)
        expected_donor_balance = Money(9.98, 'RUB')
        expected_recipient1_balance = Money(10.01, 'RUB')
        expected_recipient2_balance = Money(10.01, 'RUB')
        self.assertEqual(donor.balance, expected_donor_balance)
        self.assertEqual(recipient1.balance, expected_recipient1_balance)
        self.assertEqual(recipient2.balance, expected_recipient2_balance)

