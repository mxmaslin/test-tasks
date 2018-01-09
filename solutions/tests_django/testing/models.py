# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class QuestionSet(models.Model):
    '''
        Тест. Состоит из нескольких вопросов
    '''

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
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
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    ordering = models.PositiveSmallIntegerField(default=1, unique=True)
    is_correct = models.BooleanField()

    class Meta:
        ordering = ('ordering',)

    def __str__(self):
        return self.value


class RespondentSubmission(models.Model):
    '''
        Ответ респондента на вопрос теста
    '''
    respondent = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)

    class Meta:
        ordering = ('respondent', 'option')

    def __str__(self):
        return '{} {}'.format(self.respondent, self.option)
