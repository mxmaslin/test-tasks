from django.test import Client, TestCase

from .models import Application, Questionnaire, Submission


class PartnerAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_all_questionnaires_superuser(self):
        pass

    def test_get_all_questionnaires_partner(self):
        pass

    def test_get_all_questionnaires_bank(self):
        pass

    def test_get_all_questionnaires_wrong_guy(self):
        pass

    def test_get_questionnaire_by_id_superuser(self):
        pass

    def test_get_questionnaire_by_id_partner(self):
        pass

    def test_get_questionnaire_by_id_bank(self):
        pass

    def test_get_questionnaire_by_id_wrong_guy(self):
        pass

    def test_create_questionnaire_superuser(self):
        pass

    def test_create_questionnaire_partner(self):
        pass

    def test_create_questionnaire_bank(self):
        pass

    def test_create_questionnaire_wrong_guy(self):
        pass

    def test_modify_questionnaire_superuser(self):
        pass

    def test_modify_questionnaire_partner(self):
        pass

    def test_modify_questionnaire_bank(self):
        pass

    def test_modify_questionnaire_wrong_guy(self):
        pass

    def test_delete_questionnaire_superuser(self):
        pass

    def test_delete_questionnaire_partner(self):
        pass

    def test_delete_questionnaire_bank(self):
        pass

    def test_delete_questionnaire_wrong_guy(self):
        pass

    def test_create_submission_superuser(self):
        pass

    def test_create_submission_partner(self):
        pass

    def test_create_submission_bank(self):
        pass

    def test_create_submission_wrong_guy(self):
        pass


class BankAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_all_submissions_superuser(self):
        pass

    def test_get_all_submissions_partner(self):
        pass

    def test_get_all_submissions_bank(self):
        pass

    def test_get_all_submissions_wrong_guy(self):
        pass

    def test_get_submission_by_id_superuser(self):
        pass

    def test_get_submission_by_id_partner(self):
        pass

    def test_get_submission_by_id_bank(self):
        pass

    def test_get_submission_by_id_wrong_guy(self):
        pass

    def test_modify_submission_superuser(self):
        pass

    def test_modify_submission_partner(self):
        pass

    def test_modify_submission_bank(self):
        pass

    def test_modify_submission_wrong_guy(self):
        pass

    def test_delete_submission_superuser(self):
        pass

    def test_delete_submission_partner(self):
        pass

    def test_delete_submission_bank(self):
        pass

    def test_delete_submission_wrong_guy(self):
        pass
