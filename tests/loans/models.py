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
    rotation_started = models.DateField(blank=True, null=True)
    rotation_ended = models.DateField(blank=True, null=True)
    applicaton_name = models.CharField(max_length=255)
    application_type = models.PositiveSmallIntegerField(
        choices=APPLICATION_CHOICES,
        default=APPLICATION_CUSTOMER)
    score_min = models.PositiveSmallIntegerField(blank=True, null=True)
    score_max = models.PositiveSmallIntegerField(blank=True, null=True)
    # bank = models.ForeignKey('Bank')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Предложение по кредиту'
        verbose_name_plural = 'Предложения по кредитам'

    def __str__(self):
        return '{}'.format(self.applicaton_name, self.modified)


class Questionnaire(models.Model):
    '''
        Анкета клиента
    '''

    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    name = models.CharField(max_length=255)
    birthday = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    passport = models.CharField(max_length=255, blank=True, null=True)
    score = models.PositiveSmallIntegerField(blank=True, null=True)

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

    STATUS_CHOICES = (
        (STATUS_NEW, 'New'),
        (STATUS_SENT, 'Sent'))

    created = models.DateField(auto_now_add=True)
    submitted = models.DateField(blank=True, null=True)
    application = models.ForeignKey(Application)
    questionnaire = models.ForeignKey(Questionnaire)
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
        default=STATUS_NEW)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заявка на кредит'
        verbose_name_plural = 'Заявки на кредиты'

    def __str__(self):
        return '{}'.format(self.application)
