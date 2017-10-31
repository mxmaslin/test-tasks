# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''
        Автор либо респондент
    '''
    ROLE_AUTHOR = 0
    ROLE_RESPONDENT = 1

    ROLE_CHOICES = (
        (ROLE_AUTHOR, 'Автор'),
        (ROLE_RESPONDENT, 'Респондент'))

    name = models.CharField(max_length=20, primary_key=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=ROLE_RESPONDENT)
    question_set = models.ForeignKey('QuestionSet')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        role = ROLE_CHOICES[self.role][1]
        return '{}: {}'.format(role, self.user)


class QuestionSet(models.Model):
    '''
        Тест. Состоит из нескольких вопросов
    '''

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created', 'author')

    def __str__(self):
        return 'Автор теста: {}'.format(self.author)


class Question(models.Model):
    '''
        Является 'атомом' теста
    '''

    question = models.CharField(max_length=255)
    ordering = models.PositiveSmallIntegerField(default=1, unique=True)
    question_sets = models.ManyToManyField(QuestionSet)

    class Meta:
        ordering = ('ordering',)

    def __str__(self):
        return self.question


class Option(models.Model):
    '''
        Вариант ответа на вопрос
    '''
    question = models.ForeignKey(Question)
    value = models.CharField(max_length=255)
    ordering = models.PositiveSmallIntegerField(default=1, unique=True)
    is_correct = models.BooleanField()

    class Meta:
        ordering = ('ordering',)

    def __str__(self):
        return self.value


class Submission(models.Model):
    '''
        Ответ респондента на вопрос теста
    '''
    respondent = models.ForeignKey(User)
    option = models.OneToOneField(Option, on_delete=models.CASCADE)

    class Meta:
        ordering = ('respondent', 'option')

    def __str__(self):
        return '{} {}'.format(self.respondent, self.option)
