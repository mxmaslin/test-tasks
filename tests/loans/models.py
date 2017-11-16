# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    '''
        Суперпользователь либо партнер либо кредитная организация
    '''
    ROLE_SUPERUSER = 0
    ROLE_PARTNER = 1
    ROLE_BANK = 2

    ROLE_CHOICES = (
        (ROLE_SUPERUSER, 'Суперпользователь'),
        (ROLE_PARTNER, 'Партнер'),
        (ROLE_BANK, 'Банк'))

    name = models.CharField(max_length=20, primary_key=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=ROLE_PARTNER)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        role = User.ROLE_CHOICES[self.role][1]
        return '{}: {}'.format(role, self.name)


class Application(models.Model):
    '''
        Предложение
    '''

    APPLICATION_CUSTOMER = 0
    APPLICATION_MORTGAGE = 1
    APPLICATION_CAR = 2
    APPLICATION_BUSINESS = 3

    APPLICATION_CHOICES = (
        (APPLICATION_CUSTOMER, 'Customer'),
        (APPLICATION_MORTGAGE, 'Mortgage'),
        (APPLICATION_CAR, 'Car'),
        (APPLICATION_BUSINESS, 'Business'))

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания')
    modified = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения')
    rotation_started = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата начала ротации')
    rotation_ended = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата окончания ротации')
    application_name = models.CharField(
        max_length=255,
        verbose_name='Название предложения')
    application_type = models.PositiveSmallIntegerField(
        choices=APPLICATION_CHOICES,
        default=APPLICATION_CUSTOMER,
        verbose_name='Тип приложения')
    score_min = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Мин. скоринговый балл')
    score_max = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Макс. скоринговый балл')
    bank = models.ForeignKey(
        User,
        limit_choices_to={'role': User.ROLE_BANK})

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Предложение по кредиту'
        verbose_name_plural = 'Предложения по кредитам'

    def __str__(self):
        return '{}'.format(self.application_name, self.modified)


class Questionnaire(models.Model):
    '''
        Анкета клиента
    '''

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания')
    modified = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения')
    name = models.CharField(
        max_length=255,
        verbose_name='ФИО')
    birthday = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения')
    phone = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name='Телефон')
    passport = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Паспорт')
    score = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Скоринговый балл')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Анкета клиента'
        verbose_name_plural = 'Анкеты клиентов'

    def __str__(self):
        return '{}'.format(self.name, self.modified)


class Submission(models.Model):
    '''
        Заявка
    '''

    STATUS_NEW = 0
    STATUS_SENT = 1
    STATUS_RECEIVED = 2

    STATUS_CHOICES = (
        (STATUS_NEW, 'New'),
        (STATUS_SENT, 'Sent'),
        (STATUS_RECEIVED), 'Received')

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания')
    submitted = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата отправки')
    application = models.ForeignKey(
        Application,
        verbose_name='Предложение')
    questionnaire = models.ForeignKey(
        Questionnaire,
        verbose_name='Анкета')
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
        verbose_name='Статус заявки')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заявка на кредит'
        verbose_name_plural = 'Заявки на кредиты'

    def __str__(self):
        return '{}'.format(self.application)



from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


content_type_application = ContentType.objects.get_for_model(Application)

perm_application_view = Permission.objects.create(
    codename='can_view',
    name='Can view Applications',
    content_type=content_type_application)

perm_application_create = Permission.objects.create(
    codename='can_create',
    name='Can create Applications',
    content_type=content_type_application)

perm_application_delete = Permission.objects.create(
    codename='can_delete',
    name='Can create Applications',
    content_type=content_type_application)


content_type_questionnaire = ContentType.objects.get_for_model(Questionnaire)

perm_questionnaire_view = Permission.objects.create(
    codename='can_view',
    name='Can view Questionnaires',
    content_type=content_type_questionnaire)

perm_questionnaire_create = Permission.objects.create(
    codename='can_create',
    name='Can create Questionnaires',
    content_type=content_type_questionnaire)

perm_questionnaire_delete = Permission.objects.create(
    codename='can_delete',
    name='Can create Questionnaires',
    content_type=content_type_questionnaire)


content_type_submission = ContentType.objects.get_for_model(Submission)

perm_questionnaire_view = Permission.objects.create(
    codename='can_view',
    name='Can view Submissions',
    content_type=content_type_submission)

perm_application_create = Permission.objects.create(
    codename='can_create',
    name='Can create Questionnaire',
    content_type=content_type_questionnaire)

perm_application_delete = Permission.objects.create(
    codename='can_delete',
    name='Can create Questionnaire',
    content_type=content_type_questionnaire)
