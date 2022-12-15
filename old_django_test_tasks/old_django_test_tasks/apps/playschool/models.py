# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class StudyingRecordManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(scholar__is_studying=True)


class Scholar(models.Model):
    CHOICE_BOY = 'M'
    CHOICE_GIRL = 'F'

    SEX_CHOICES = (
        (CHOICE_BOY, 'Boy'),
        (CHOICE_GIRL, 'Girl'))

    photo = models.ImageField(upload_to='playschool/images/%Y/%m/%d', blank=True, null=True)
    name = models.CharField(max_length=50)
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        default=CHOICE_GIRL)
    birth_date = models.DateField()
    school_class = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(11)])
    is_studying = models.BooleanField()

    class Meta:
        ordering = ('school_class', 'name')

    def __str__(self):
        return f'{self.name}, {self.birth_date}, {self.school_class}'


class Record(models.Model):
    CHOICE_MOTHER = 'M'
    CHOICE_FATHER = 'F'

    PARENT_CHOICES = (
        (CHOICE_MOTHER, 'Mother'),
        (CHOICE_FATHER, 'Father'))

    scholar = models.ForeignKey(Scholar, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    has_came_with = models.CharField(
        max_length=1,
        choices=PARENT_CHOICES,
        default=CHOICE_MOTHER)
    time_arrived = models.DateTimeField()
    time_departed = models.DateTimeField()

    objects = models.Manager()
    studying = StudyingRecordManager()

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f'{self.date}, {self.scholar}'
