import base64
import json
from django.test import Client, TestCase

from .models import Application, Questionnaire, Submission


class PartnerAPITestCase(TestCase):
    fixtures = ['loans']

    def setUp(self):
        self.client = Client()

    def test_get_all_questionnaires_superuser(self):
        self.client.login(
            username='superuser',
            password='qwer1234')
        response = self.client.get('/loans/partner_api/questionnaires/')
        self.client.logout()
        self.assertEqual(response.status_code, 200)

    def test_get_all_questionnaires_partner(self):
        self.client.login(
            username='partner',
            password='qwer1234')
        response = self.client.get('/loans/partner_api/questionnaires/')
        self.client.logout()
        self.assertEqual(response.status_code, 200)

    def test_get_all_questionnaires_bank(self):
        self.client.login(
            username='bank',
            password='qwer1234')
        response = self.client.get('/loans/partner_api/questionnaires/')
        self.client.logout()
        self.assertEqual(response.status_code, 200)

    def test_get_all_questionnaires_wrong_guy(self):
        self.client.login(
            username='wrong_guy',
            password='qwer1234')
        response = self.client.get('/loans/partner_api/questionnaires/')
        self.client.logout()
        self.assertEqual(response.status_code, 403)

    def test_get_questionnaire_by_id_superuser(self):
        self.client.login(
            username='superuser',
            password='qwer1234')
        response = self.client.get('/loans/partner_api/questionnaires/1/')
        self.client.logout()
        self.assertEqual(response.status_code, 200)

    def test_get_questionnaire_by_id_partner(self):
        self.client.login(
            username='partner',
            password='qwer1234')
        response = self.client.get('/loans/partner_api/questionnaires/1/')
        self.client.logout()
        self.assertEqual(response.status_code, 200)

    def test_get_questionnaire_by_id_bank(self):
        self.client.login(
            username='bank',
            password='qwer1234')
        response = self.client.get('/loans/partner_api/questionnaires/1/')
        self.client.logout()
        self.assertEqual(response.status_code, 200)

    def test_get_questionnaire_by_id_wrong_guy(self):
        self.client.login(
            username='wrong_guy',
            password='qwer1234')
        response = self.client.get('/loans/partner_api/questionnaires/1/')
        self.client.logout()
        self.assertEqual(response.status_code, 403)

    def test_create_questionnaire_superuser(self):
        self.client.login(
            username='superuser',
            password='qwer1234')
        response = self.client.post(
            '/loans/partner_api/questionnaires/',
            {'name': 'John Doe'})
        self.client.logout()
        self.assertEqual(response.status_code, 201)

    def test_create_questionnaire_partner(self):
        self.client.login(
            username='partner',
            password='qwer1234')
        response = self.client.post(
            '/loans/partner_api/questionnaires/',
            {'name': 'John Doe'})
        self.client.logout()
        self.assertEqual(response.status_code, 201)

    def test_create_questionnaire_bank(self):
        self.client.login(
            username='bank',
            password='qwer1234')
        response = self.client.post(
            '/loans/partner_api/questionnaires/',
            {'name': 'John Doe'})
        self.client.logout()
        self.assertEqual(response.status_code, 201)

    def test_create_questionnaire_wrong_guy(self):
        self.client.login(
            username='wrong_guy',
            password='qwer1234')
        response = self.client.post(
            '/loans/partner_api/questionnaires/',
            {'name': 'John Doe'})
        self.client.logout()
        self.assertEqual(response.status_code, 403)

    def test_modify_questionnaire_superuser(self):
        self.client.login(
            username='superuser',
            password='qwer1234')
        response = self.client.put(
            '/loans/partner_api/questionnaires/1/',
            '{"name": "Jane Doe"}',
            'application/json',
            )
        self.client.logout()
        self.assertEqual(response.status_code, 200)

    def test_modify_questionnaire_partner(self):
        self.client.login(
            username='partner',
            password='qwer1234')
        response = self.client.put(
            '/loans/partner_api/questionnaires/1/',
            '{"name": "Jane Doe"}',
            'application/json',
            )
        self.client.logout()
        self.assertEqual(response.status_code, 403)

    def test_modify_questionnaire_bank(self):
        self.client.login(
            username='bank',
            password='qwer1234')
        response = self.client.put(
            '/loans/partner_api/questionnaires/1/',
            '{"name": "Jane Doe"}',
            'application/json',
            )
        self.client.logout()
        self.assertEqual(response.status_code, 403)

    def test_modify_questionnaire_wrong_guy(self):
        self.client.login(
            username='wrong_guy',
            password='qwer1234')
        response = self.client.put(
            '/loans/partner_api/questionnaires/1/',
            '{"name": "Jane Doe"}',
            'application/json',
            )
        self.client.logout()
        self.assertEqual(response.status_code, 403)

    def test_delete_questionnaire_superuser(self):
        self.client.login(
            username='superuser',
            password='qwer1234')
        response = self.client.delete(
            '/loans/partner_api/questionnaires/1/')
        self.client.logout()
        self.assertEqual(response.status_code, 204)

    def test_delete_questionnaire_partner(self):
        self.client.login(
            username='partner',
            password='qwer1234')
        response = self.client.delete(
            '/loans/partner_api/questionnaires/1/')
        self.client.logout()
        self.assertEqual(response.status_code, 403)

    def test_delete_questionnaire_bank(self):
        self.client.login(
            username='bank',
            password='qwer1234')
        response = self.client.delete(
            '/loans/partner_api/questionnaires/1/')
        self.client.logout()
        self.assertEqual(response.status_code, 403)

    def test_delete_questionnaire_wrong_guy(self):
        self.client.login(
            username='wrong_guy',
            password='qwer1234')
        response = self.client.delete(
            '/loans/partner_api/questionnaires/1/')
        self.client.logout()
        self.assertEqual(response.status_code, 403)

    def test_create_submission_superuser(self):
        self.client.login(
            username='superuser',
            password='qwer1234')
        response = self.client.post(
            '/loans/partner_api/make_submission/', {
                "application": 1,
                "questionnaire": 1,
                "status": 1,
                "created": "2017-11-10T18:23:16.913526Z",
                "submitted": "2017-11-10T18:23:16.913526Z"})
        self.client.logout()
        self.assertEqual(response.status_code, 201)

    def test_create_submission_partner(self):
        self.client.login(
            username='partner',
            password='qwer1234')
        response = self.client.post(
            '/loans/partner_api/make_submission/', {
                "application": 1,
                "questionnaire": 1,
                "status": 1,
                "created": "2017-11-10T18:23:16.913526Z",
                "submitted": "2017-11-10T18:23:16.913526Z"})
        self.client.logout()
        self.assertEqual(response.status_code, 201)

    def test_create_submission_bank(self):
        self.client.login(
            username='bank',
            password='qwer1234')
        response = self.client.post(
            '/loans/partner_api/make_submission/', {
                "application": 1,
                "questionnaire": 1,
                "status": 1,
                "created": "2017-11-10T18:23:16.913526Z",
                "submitted": "2017-11-10T18:23:16.913526Z"})
        self.client.logout()
        self.assertEqual(response.status_code, 201)

    def test_create_submission_wrong_guy(self):
        self.client.login(
            username='wrong_guy',
            password='qwer1234')
        response = self.client.post(
            '/loans/partner_api/make_submission/', {
                "application": 1,
                "questionnaire": 1,
                "status": 1,
                "created": "2017-11-10T18:23:16.913526Z",
                "submitted": "2017-11-10T18:23:16.913526Z"})
        self.client.logout()
        self.assertEqual(response.status_code, 403)


class BankAPITestCase(TestCase):
    fixtures = ['loans']

    def setUp(self):
        self.client = Client()

    def test_get_all_submissions_superuser(self):
        self.client.login(
            username='superuser',
            password='qwer1234')
        response = self.client.get('/loans/bank_api/submissions/')
        self.client.logout()
        self.assertEqual(response.status_code, 403)

    def test_get_all_submissions_partner(self):
        self.client.login(
            username='partner',
            password='qwer1234')
        response = self.client.get('/loans/bank_api/submissions/')
        self.client.logout()
        self.assertEqual(response.status_code, 403)

    def test_get_all_submissions_bank(self):
        self.client.login(
            username='bank',
            password='qwer1234')
        response = self.client.get('/loans/bank_api/submissions/')
        self.client.logout()
        self.assertEqual(response.status_code, 200)

    def test_get_all_submissions_wrong_guy(self):
        self.client.login(
            username='wrong_guy',
            password='qwer1234')
        response = self.client.get('/loans/bank_api/submissions/')
        self.client.logout()
        self.assertEqual(response.status_code, 403)

    def test_get_submission_by_id_superuser(self):
        self.client.login(
            username='superuser',
            password='qwer1234')
        response = self.client.get('/loans/bank_api/submissions/1/')
        self.client.logout()
        self.assertEqual(response.status_code, 403)

    def test_get_submission_by_id_partner(self):
        self.client.login(
            username='partner',
            password='qwer1234')
        response = self.client.get('/loans/bank_api/submissions/1/')
        self.client.logout()
        self.assertEqual(response.status_code, 403)

    def test_get_submission_by_id_bank(self):
        self.client.login(
            username='bank',
            password='qwer1234')
        response = self.client.get('/loans/bank_api/submissions/1/')
        self.client.logout()
        self.assertEqual(response.status_code, 200)

    def test_get_submission_by_id_wrong_guy(self):
        self.client.login(
            username='wrong_guy',
            password='qwer1234')
        response = self.client.get('/loans/bank_api/submissions/1/')
        self.client.logout()
        self.assertEqual(response.status_code, 403)

    def test_modify_submission_superuser(self):
        self.client.login(
            username='superuser',
            password='qwer1234')
        response = self.client.put(
            '/loans/bank_api/submissions/1/',
            '{"application": 1, "questionnaire": 1, "status": 2}',
            'application/json',
            )
        self.client.logout()
        self.assertEqual(response.status_code, 200)

    def test_modify_submission_partner(self):
        self.client.login(
            username='partner',
            password='qwer1234')
        response = self.client.put(
            '/loans/bank_api/submissions/1/',
            '{"application": 1, "questionnaire": 1, "status": 2}',
            'application/json',
            )
        self.client.logout()
        self.assertEqual(response.status_code, 403)

    def test_modify_submission_bank(self):
        self.client.login(
            username='bank',
            password='qwer1234')
        response = self.client.put(
            '/loans/bank_api/submissions/1/',
            '{"application": 1, "questionnaire": 1, "status": 2}',
            'application/json',
            )
        self.client.logout()
        self.assertEqual(response.status_code, 403)

    def test_modify_submission_wrong_guy(self):
        self.client.login(
            username='wrong_guy',
            password='qwer1234')
        response = self.client.put(
            '/loans/bank_api/submissions/1/',
            '{"application": 1, "questionnaire": 1, "status": 2}',
            'application/json',
            )
        self.client.logout()
        self.assertEqual(response.status_code, 403)

    def test_delete_submission_superuser(self):
        self.client.login(
            username='superuser',
            password='qwer1234')
        response = self.client.delete(
            '/loans/bank_api/submissions/1/')
        self.client.logout()
        self.assertEqual(response.status_code, 204)

    def test_delete_submission_partner(self):
        self.client.login(
            username='partner',
            password='qwer1234')
        response = self.client.delete(
            '/loans/bank_api/submissions/1/')
        self.client.logout()
        self.assertEqual(response.status_code, 403)

    def test_delete_submission_bank(self):
        self.client.login(
            username='bank',
            password='qwer1234')
        response = self.client.delete(
            '/loans/bank_api/submissions/1/')
        self.client.logout()
        self.assertEqual(response.status_code, 403)

    def test_delete_submission_wrong_guy(self):
        self.client.login(
            username='wrong_guy',
            password='qwer1234')
        response = self.client.delete(
            '/loans/bank_api/submissions/1/')
        self.client.logout()
        self.assertEqual(response.status_code, 403)
