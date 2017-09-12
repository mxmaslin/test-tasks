# -*- coding: utf-8 -*-
from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=255)
    ordering = models.PositiveSmallIntegerField(default=1, unique=True)
    tests = models.ManyToManyField('Test')

    class Meta:
        ordering = ('ordering',)

    def __str__(self):
        return self.question


class Answer(models.Model):
    answer = models.CharField(max_length=255)
    question = models.ForeignKey(Question)
    ordering = models.PositiveSmallIntegerField(default=1, unique=True)
    is_correct = models.BooleanField()

    class Meta:
        ordering = ('ordering',)

    def __str__(self):
        return self.answer


class Test(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created', 'author')

    def __str__(self):
        return self.author


class Author(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Respondent(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    tests = models.ManyToManyField(Test)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Grade(models.Model):
    grade = models.PositiveSmallIntegerField(default=0)
    test = models.ForeignKey(Test)
    respondent = models.ForeignKey(Respondent)

    class Meta:
        ordering = ('respondent', 'grade')

    def __str__(self):
        return '{}, {}, {}'.format(self.respondent, self.test, self.grade)


class RespondentAnswer(models.Model):
    respondent = models.ForeignKey(Respondent)
    answer = models.OneToOneField(Answer, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
