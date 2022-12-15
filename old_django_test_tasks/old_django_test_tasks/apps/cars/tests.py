import json

from rest_framework.test import APIClient, APITestCase


class CarAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_car_data(self):
        self.client.post(
            '/cars/car/',
            {
                'uid': '1',
                'color': 'red',
                'vendor': 'VW',
                'model': 'Polo',
                'engine_identifier': '12345',
                'mileage': 10000
            },
            format='json')
        self.client.post(
            '/cars/component/',
            {
                'uid': '1',
                'car': '1',
                'type': 0
            },
            format='json')
        self.client.post(
            '/cars/trip/',
            {
                'car': '1',
                'distance': 10000,
                'start_date': '2018-09-22T15:22:59.131129+03:00',
                'end_date': '2018-09-22T15:22:59.131129+03:00',
            },
            format='json')
        car_data = self.client.get('/cars/car/1/').json()
        expected_data = {
            'pk': 1,
            'uid': '1',
            'color': 'red',
            'vendor': 'VW',
            'model': 'Polo',
            'engine_identifier': '12345',
            'mileage': 10000,
            'trip_set': [{
                'pk': 1,
                'car': '1',
                'distance': 10000,
                'start_date': '2018-09-22T15:22:59.131129+03:00',
                'end_date': '2018-09-22T15:22:59.131129+03:00'
            }],
            'component_set': [{
                'pk': 1,
                'uid': '1',
                'car': '1',
                'type': 0
            }]
        }
        self.assertEqual(car_data, expected_data)
