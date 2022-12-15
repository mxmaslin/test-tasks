import os

from rest_framework.test import APIClient, APITestCase

from .models import Record


class ScholarAPITestCase(APITestCase):
    fixtures = ['playschool']

    def setUp(self):
        self.client = APIClient()

    def test_create(self):
        path_to_photo = os.path.join(os.getcwd(), 'media/playschool/images/2018/09/22/cat.png')
        file = open(path_to_photo, 'rb')
        request = self.client.post(
            '/playschool/scholars/',
            {
                'photo': file,
                'name': 'Vasiliy',
                'sex': 'M',
                'birth_date': '2018-1-31',
                'school_class': 1,
                'is_studying': True
            },
            format='multipart')
        self.assertEqual(request.status_code, 201)


class RecordAPITestCase(APITestCase):
    fixtures = ['playschool']

    def setUp(self):
        self.client = APIClient()

    def test_create(self):
        request = self.client.post(
            '/playschool/records/',
            {
                "scholar": 7,
                "date": "2018-06-27",
                "has_come_with": "M",
                "time_arrived": "2018-06-27T08:56:19Z",
                "time_departed": "2018-06-27T08:56:20Z"
            },
            format='json')
        self.assertEqual(request.status_code, 201)

    def test_update(self):
        request = self.client.put(
            '/playschool/records/4/',
            {
                "scholar": 7,
                "date": "2016-06-27",
                "has_come_with": "F",
                "time_arrived": "2018-06-27T08:56:19Z",
                "time_departed": "2018-06-27T08:56:20Z"
            },
            format='json')
        self.assertEqual(request.status_code, 200)

    def test_get_studying_amount(self):
        studying = Record.studying.all().count()
        self.assertEqual(studying, 1)

    def test_get_studying_pk_exists(self):
        has_studying = Record.studying.filter(pk=4).exists()
        self.assertEqual(has_studying, True)

    def test_get_studying_pk_not_exists(self):
        # record pk 5 is not studying
        has_studying = Record.studying.filter(pk=5).exists()
        self.assertEqual(has_studying, False)
