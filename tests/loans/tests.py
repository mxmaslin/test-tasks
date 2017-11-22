# -*- coding: utf-8 -*-
# from django.test import TestCase
import unittest
from django.test import Client
from .models import Application, Questionnaire, Submission
from django.contrib.auth.models import User

superuser = User.objects.get(username='superuser')
partner = User.objects.get(username='partner')
bank = User.objects.get(username='bank')


def create_questionnaire(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return Questionnaire.objects.create(**defaults)


def create_submission(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return Submission.objects.create(**defaults)


class QuestionnaireViewTest(unittest.TestCase):
    '''
        Тесты для Questionnaire
    '''
    def setUp(self):
        self.client = Client()
        self.questionnaire = create_questionnaire(data)

    def test_list_questionnaire(self):
        url = 'my_url'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_questionnaire(self):
        url = 'my_url'
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_questionnaire(self):
        url = 'my_url'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_questionnaire(self):
        url = 'my_url'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class SubmissionViewTest(unittest.TestCase):
    '''
        Тесты для Submission
    '''
    def setUp(self):
        self.client = Client()
        self.submission = create_submission()

    def test_list_submission(self):
        url = 'my_url'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_submission(self):
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_submission(self):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_submission(self):
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
