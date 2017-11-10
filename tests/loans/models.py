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

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('loans_application_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('loans_application_update', args=(self.pk,))


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

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('loans_questionnaire_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('loans_questionnaire_update', args=(self.pk,))


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

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('loans_submission_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('loans_submission_update', args=(self.pk,))
