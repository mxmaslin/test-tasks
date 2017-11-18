from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        superusers = Group.objects.create(name='Суперпользователи')
        partners = Group.objects.create(name='Партнёры')
        banks = Group.objects.create(name='Банки')

        perm_add_questionnaire = Permission.objects.get(
            codename='add_questionnaire')
        perm_edit_questionnaire = Permission.objects.get(
            codename='change_questionnaire')
        perm_delete_questionnaire = Permission.objects.get(
            codename='change_questionnaire')

        superpupers.permissions.add(perm_add_questionnaire)
        superpupers.permissions.add(perm_edit_questionnaire)
        superpupers.permissions.add(perm_delete_questionnaire)
