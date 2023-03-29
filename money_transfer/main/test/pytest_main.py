import pytest
from django.urls import reverse
from djmoney.money import Money
from rest_framework import status
from rest_framework.test import APIClient

from main.models import PaymentUser

INITIAL_BALANCE = Money(1000, 'RUB')


@pytest.fixture
def user1(db):
    inn = '1234567890'
    return PaymentUser.objects.create_user(
        username=inn, inn=inn, balance=INITIAL_BALANCE
    )


@pytest.fixture
def user2(db):
    inn = '1234567891'
    return PaymentUser.objects.create_user(
        username=inn, inn=inn, balance=INITIAL_BALANCE
    )


@pytest.fixture
def user3(db):
    inn = '1234567892'
    return PaymentUser.objects.create_user(
        username=inn, inn=inn, balance=INITIAL_BALANCE
    )


@pytest.mark.parametrize(
    'sent,expected', [
        (0, (1000, 1000, 1000)),
        (0.01, (1000, 1000, 1000)),
        (0.02, (1000, 1000, 1000)),
        (3, (998, 1001, 1001)),
        (0.3, (999.8, 1000.1, 1000.1)),
        (0.33, (999.78, 1000.11, 1000.11)),
        (4, (997.34, 1001.33, 1001.33)),
        (4.4, (997.08, 1001.46, 1001.46)),
        (4.44, (997.04, 1001.48, 1001.48)),
        (400, (733.34, 1133.33, 1133.33)),
    ]
)
@pytest.mark.django_db(transaction=True)
def test_sending_including_self(sent, expected, user1, user2, user3):
    url = f'{reverse("money_transfer", kwargs={"inn": user1.inn})}'
    data = {
        'send_sum': sent,
        'recipients': ['1234567890', '1234567891', '1234567892']
    }
    client = APIClient()
    response = client.post(url, data)
    assert response.status_code == status.HTTP_200_OK

    recipient1 = PaymentUser.objects.get(inn=user1.inn)
    recipient2 = PaymentUser.objects.get(inn=user2.inn)
    recipient3 = PaymentUser.objects.get(inn=user3.inn)
    recipient1_expected, recipient2_expected, recipient3_expected = expected
    assert recipient1.balance == Money(recipient1_expected, 'RUB')
    assert recipient2.balance == Money(recipient2_expected, 'RUB')
    assert recipient3.balance == Money(recipient3_expected, 'RUB')


@pytest.mark.parametrize(
    'sent,expected', [
        (0, (1000, 1000, 1000)),
        (0.01, (1000, 1000, 1000)),
        (0.02, (999.98, 1000.01, 1000.01)),
        (0.03, (999.98, 1000.01, 1000.01)),
        (2, (998, 1001, 1001)),
        (0.2, (999.8, 1000.1, 1000.1)),
        (0.22, (999.78, 1000.11, 1000.11)),
        (30, (970, 1015, 1015)),
        (30.01, (970, 1015, 1015)),
        (1.03, (998.98, 1000.51, 1000.51)),
    ]
)
@pytest.mark.django_db(transaction=True)
def test_sending_excluding_self(sent, expected, user1, user2, user3):
    url = f'{reverse("money_transfer", kwargs={"inn": user1.inn})}'
    data = {
        'send_sum': sent,
        'recipients': ['1234567891', '1234567892']
    }
    client = APIClient()
    response = client.post(url, data)
    assert response.status_code == status.HTTP_200_OK

    recipient1 = PaymentUser.objects.get(inn=user1.inn)
    recipient2 = PaymentUser.objects.get(inn=user2.inn)
    recipient3 = PaymentUser.objects.get(inn=user3.inn)
    recipient1_expected, recipient2_expected, recipient3_expected = expected
    assert recipient1.balance == Money(recipient1_expected, 'RUB')
    assert recipient2.balance == Money(recipient2_expected, 'RUB')
    assert recipient3.balance == Money(recipient3_expected, 'RUB')
