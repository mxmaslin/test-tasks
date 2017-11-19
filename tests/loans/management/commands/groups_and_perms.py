from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        superusers = Group.objects.create(name='Суперпользователи')
        partners = Group.objects.create(name='Партнёры')
        banks = Group.objects.create(name='Кредитные организации')

        perm_view_application = Permission.objects.get(
            codename='view_application')
        perm_add_application = Permission.objects.get(
            codename='add_application')
        perm_change_application = Permission.objects.get(
            codename='change_application')
        perm_delete_application = Permission.objects.get(
            codename='delete_application')

        perm_view_questionnaire = Permission.objects.get(
            codename='view_questionnaire')
        perm_add_questionnaire = Permission.objects.get(
            codename='add_questionnaire')
        perm_change_questionnaire = Permission.objects.get(
            codename='change_questionnaire')
        perm_delete_questionnaire = Permission.objects.get(
            codename='delete_questionnaire')

        perm_view_submission = Permission.objects.get(
            codename='view_submission')
        perm_add_submission = Permission.objects.get(
            codename='add_submission')
        perm_change_submission = Permission.objects.get(
            codename='change_submission')
        perm_delete_submission = Permission.objects.get(
            codename='delete_submission')

        superusers.permissions.add(perm_view_questionnaire)
        superusers.permissions.add(perm_add_questionnaire)
        superusers.permissions.add(perm_edit_questionnaire)
        superusers.permissions.add(perm_delete_questionnaire)

        superusers.permissions.add(perm_edit_submission)
        superusers.permissions.add(perm_delete_submission)

        partners.permissions.add(perm_view_questionnaire)

        banks.permissions.add(perm_view_submission)
