# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Child(models.Model):
    CHOICE_BOY = 'M'
    CHOICE_GIRL = 'F'

    SEX_CHOICES = (
        (CHOICE_BOY, 'Boy'),
        (CHOICE_GIRL, 'Girl'))

    photo = models.ImageField(upload_to='images/%Y/%m/%d')
    name = models.CharField(max_length=50)
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        default=CHOICE_GIRL)
    birth_date = models.DateField()
    school_class = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(11)])
    is_in_school = models.BooleanField()

    class Meta:
        ordering = ('school_class', 'name')

    def __str__(self):
        return f'{self.name}, {self.birth_date}, {self.school_class}'


class Log(models.Model):
    CHOICE_MOTHER = 'M'
    CHOICE_FATHER = 'F'

    PARENT_CHOICES = (
        (CHOICE_MOTHER, 'Mother'),
        (CHOICE_FATHER, 'Father'))

    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    has_come_with = models.CharField(
        max_length=1,
        choices=PARENT_CHOICES,
        default=CHOICE_MOTHER)
    time_arrived = models.DateTimeField()
    time_departed = models.DateTimeField()

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f'{self.date}, {self.child}'
