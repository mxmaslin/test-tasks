# -*- coding: utf-8 -*-
# from django.test import TestCase
import unittest
from django.test import Client
from .models import Application, Questionnaire, Submission
from django.contrib.auth.models import User

# superuser = User.objects.get(username='superuser')
# partner = User.objects.get(username='partner')
# bank = User.objects.get(username='bank')


def create_questionnaire(**kwargs):
    return Questionnaire.objects.create(**kwargs)


def create_submission(**kwargs):
    return Submission.objects.create(**kwargs)


class QuestionnaireViewTest(unittest.TestCase):
    '''
        Тесты для Questionnaire
    '''
    def setUp(self):
        self.client = Client()
        self.questionnaire = create_questionnaire(
            "name": "Давид Соломонович",
            "birthday": "1957-06-21",
            "passport": "abc123", "phone":
            "130-19-32",
            "score": 5)
        self.url = 'http://127.0.0.1/loans/partner_api/questionnaires/'

    def test_list_questionnaire(self):
        response = self.client.get(
            self.url,
            {'username': 'superuser', 'password': 'qwer1234'})
        self.assertEqual(response.status_code, 200)

#     def test_create_questionnaire(self):
#         url = 'my_url'
#         response = self.client.post(url, data=data)
#         self.assertEqual(response.status_code, 302)

#     def test_detail_questionnaire(self):
#         url = 'my_url'
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)

#     def test_update_questionnaire(self):
#         url = 'my_url'
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 302)


# class SubmissionViewTest(unittest.TestCase):
#     '''
#         Тесты для Submission
#     '''
#     def setUp(self):
#         self.client = Client()
#         self.submission = create_submission(
#             "application": 1,
#             "questionnaire": 1,
#             "status": 2)

#     def test_list_submission(self):
#         url = 'my_url'
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)

#     def test_create_submission(self):
#         response = self.client.post(url, data=data)
#         self.assertEqual(response.status_code, 302)

#     def test_detail_submission(self):
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)

#     def test_update_submission(self):
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 302)
