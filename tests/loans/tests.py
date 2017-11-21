# -*- coding: utf-8 -*-
# from django.test import TestCase
import unittest
from django.core.urlresolvers import reverse
from django.test import Client
from .models import Application, Questionnaire, Submission
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType


def create_django_contrib_auth_models_user(**kwargs):
    defaults = {}
    defaults["username"] = "username"
    defaults["email"] = "username@tempurl.com"
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_django_contrib_auth_models_group(**kwargs):
    defaults = {}
    defaults["name"] = "group"
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_django_contrib_contenttypes_models_contenttype(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_application(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    if "bank" not in defaults:
        defaults["bank"] = create_user()
    return Application.objects.create(**defaults)


def create_questionnaire(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return Questionnaire.objects.create(**defaults)


def create_submission(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return Submission.objects.create(**defaults)


class ApplicationViewTest(unittest.TestCase):
    '''
    Tests for Application
    '''
    def setUp(self):
        self.client = Client()

    def test_list_application(self):
        url = reverse('app_name_application_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_application(self):
        url = reverse('app_name_application_create')
        data = {
            "bank": create_user().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_application(self):
        application = create_application()
        url = reverse('app_name_application_detail', args=[application.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_application(self):
        application = create_application()
        data = {
            "bank": create_user().pk,
        }
        url = reverse('app_name_application_update', args=[application.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class QuestionnaireViewTest(unittest.TestCase):
    '''
    Tests for Questionnaire
    '''
    def setUp(self):
        self.client = Client()

    def test_list_questionnaire(self):
        url = reverse('app_name_questionnaire_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_questionnaire(self):
        url = reverse('app_name_questionnaire_create')
        data = {
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_questionnaire(self):
        questionnaire = create_questionnaire()
        url = reverse('app_name_questionnaire_detail', args=[questionnaire.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_questionnaire(self):
        questionnaire = create_questionnaire()
        data = {
        }
        url = reverse('app_name_questionnaire_update', args=[questionnaire.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class SubmissionViewTest(unittest.TestCase):
    '''
    Tests for Submission
    '''
    def setUp(self):
        self.client = Client()

    def test_list_submission(self):
        url = reverse('app_name_submission_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_submission(self):
        url = reverse('app_name_submission_create')
        data = {
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_submission(self):
        submission = create_submission()
        url = reverse('app_name_submission_detail', args=[submission.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_submission(self):
        submission = create_submission()
        data = {
        }
        url = reverse('app_name_submission_update', args=[submission.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)