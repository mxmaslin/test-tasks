from django.test import Client, TestCase


class ScholarAPITestCase(TestCase):
    # fixtures = ['playschool']

    def setUp(self):
        self.client = Client()

    def test_create(self):
        response = self.client.post(
            '/playschool/scholars/',
            {
                'photo': '?',
                'name': 'Vasiliy',
                'sex': 'M',
                'birth_date': '2018-1-31',
                'school_class': 1,
                'is_studying': True
            })
        print(response.reason_phrase)
        self.assertEqual(response.status_code, 201)
