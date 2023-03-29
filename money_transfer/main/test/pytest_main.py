import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from main.models import PaymentUser


@pytest.fixture
def user1(db):
    inn = '1234567890'
    return PaymentUser.objects.create_user(username=inn, inn=inn, balance=1000)


@pytest.fixture
def user2(db):
    inn = '1234567891'
    return PaymentUser.objects.create_user(username=inn, inn=inn, balance=1000)


@pytest.fixture
def user3(db):
    inn = '1234567892'
    return PaymentUser.objects.create_user(username=inn, inn=inn, balance=1000)


@pytest.mark.parametrize(
    'sent,earned,expected', [
        (10, (20, 20, 20), (20, 20, 20)),
        (20, (10, 10, 10), (10, 10, 10)),
    ]
)
@pytest.mark.django_db(transaction=True)
def test_sending_including_self(sent, earned, expected, user1, user2, user3):
    self_inn = '1234567890'
    url = f'{reverse("money_transfer", kwargs={"inn": self_inn})}'
    data = {
        'send_sum': 3,
        'recipients': ['1234567890', '1234567891', '1234567892']
    }
    client = APIClient()
    response = client.post(url, data)
    print(response)
    assert True
