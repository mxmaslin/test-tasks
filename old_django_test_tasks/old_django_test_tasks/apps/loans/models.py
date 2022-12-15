# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from dry_rest_permissions.generics import authenticated_users


class Offer(models.Model):
    """
        Предложение банка
    """
    OFFER_CHOICES = (
        (0, 'Customer'),
        (1, 'Mortgage'),
        (2, 'Car'),
        (3, 'Business'))

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
    offer_name = models.CharField(
        max_length=255,
        verbose_name='Название предложения')
    offer_type = models.PositiveSmallIntegerField(
        choices=OFFER_CHOICES,
        default=0,
        verbose_name='Тип предложения')
    score_min = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Мин. скоринговый балл')
    score_max = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Макс. скоринговый балл')
    bank = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Предложение по кредиту'
        verbose_name_plural = 'Предложения по кредитам'

    def __str__(self):
        return '{}'.format(self.offer_name, self.modified)


class Questionnaire(models.Model):
    """
        Анкета клиента
    """

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

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @authenticated_users
    def has_write_permission(request):
        return True

    @staticmethod
    @authenticated_users
    def has_update_permission(request):
        return True

    def has_object_update_permission(self, request):
        return request.user.groups.filter(
            name='Суперпользователи').exists()

    def has_object_destroy_permission(self, request):
        return request.user.groups.filter(
            name='Суперпользователи').exists()


class Submission(models.Model):
    """
        Заявка на кредит
    """
    STATUS_CHOICES = (
        (0, 'New'),
        (1, 'Sent'),
        (2, 'Received'))

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания')
    submitted = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата отправки')
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        verbose_name='Предложение')
    questionnaire = models.ForeignKey(
        Questionnaire,
        on_delete=models.CASCADE,
        verbose_name='Анкета')
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
        default=0,
        verbose_name='Статус заявки')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заявка на кредит'
        verbose_name_plural = 'Заявки на кредиты'

    def __str__(self):
        return '{}'.format(self.offer)

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return request.user.groups.filter(
            name='Кредитные организации').exists()

    def has_object_read_permission(self, request):
        return request.user.groups.filter(
            name='Кредитные организации').exists()

    @staticmethod
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.groups.filter(
                name='Суперпользователи').exists(),
            request.user.groups.filter(
                name='Партнёры').exists(),
            request.user.groups.filter(
                name='Кредитные организации').exists()])

    @staticmethod
    @authenticated_users
    def has_update_permission(request):
        return True

    def has_object_update_permission(self, request):
        return request.user.groups.filter(
            name='Суперпользователи').exists()

    def has_object_destroy_permission(self, request):
        return request.user.groups.filter(
            name='Суперпользователи').exists()
