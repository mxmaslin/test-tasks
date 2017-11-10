# -*- coding: utf-8 -*-
from django.db import models


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

    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    rotation_started = models.DateField(editable=False)
    rotation_ended = models.DateField(editable=False)
    applicaton_name = models.CharField(max_length=255)
    application_type = models.PositiveSmallIntegerField(
        choices=APPLICATION_CHOICES,
        default=APPLICATION_CUSTOMER)
    score_min = models.PositiveSmallIntegerField()
    score_max = models.PositiveSmallIntegerField()
    # bank = models.ForeignKey('Bank')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{}'.format(self.applicaton_name, self.modified)


class Questionnaire(models.Model):
    '''
        Анкета клиента
    '''

    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    name = models.CharField(max_length=255)
    birthday = models.DateField()
    phone = models.CharField(max_length=10)
    passport = models.CharField(max_length=255)
    score = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{}'.format(self.name, self.modified)


class Submission(models.Model):
    '''
        Заявка
    '''

    STATUS_NEW = 0
    STATUS_SENT = 1

    STATUS_CHOICES = (
        (STATUS_NEW, 'New'),
        (STATUS_SENT, 'Sent'))

    created = models.DateField(auto_now_add=True)
    submitted = models.DateField()
    application = models.ForeignKey(Application)
    questionnaire = models.ForeignKey(Questionnaire)
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
        default=STATUS_NEW)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{}'.format(self.application)
