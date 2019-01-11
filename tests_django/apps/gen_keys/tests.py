from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Key


class AccountTests(APITestCase):

    fixtures = ['keys.json']

    def test_create_key(self):
        url = reverse('gen_keys:keys_list')
        response = self.client.post(url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_keys(self):
        url = reverse('gen_keys:keys_list')
        response = self.client.get(url, format='json')
        non_provided_amount = Key.objects.filter(is_provided=False).count()
        non_provided_amount_expected = len(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(non_provided_amount_expected, non_provided_amount)

    def test_expire_provided_key(self):
        provided_key = Key.objects.get(is_provided=True, is_expired=False)
        provided_key_pk = provided_key.pk
        url = reverse('gen_keys:key_detail', kwargs={'pk': provided_key_pk})
        response = self.client.put(url, format='json')
        expired_key = Key.objects.get(pk=provided_key_pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expired_key.is_expired, True)

    def test_expire_not_provided_key(self):
        not_provided_key = Key.objects.filter(is_provided=False).first()
        not_provided_key_pk = not_provided_key.pk
        url = reverse('gen_keys:key_detail', kwargs={'pk': not_provided_key_pk})
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_multiple_expire_provided_key(self):
        provided_key = Key.objects.get(is_provided=True, is_expired=False)
        provided_key_pk = provided_key.pk
        url = reverse('gen_keys:key_detail', kwargs={'pk': provided_key_pk})
        response = self.client.put(url, format='json')
        expired_key = Key.objects.get(pk=provided_key_pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expired_key.is_expired, True)
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
