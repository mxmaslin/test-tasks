from datetime import datetime

from django.db import models


class Car(models.Model):
    uid = models.CharField(max_length=10, unique=True)
    color = models.CharField(max_length=20)
    vendor = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    engine_identifier = models.CharField(max_length=20, unique=True)
    mileage = models.IntegerField()


class Component(models.Model):
    COMPONENTS = (
        (0, 'engine'),
        (1, 'body'),
        (2, 'electrical'),
        (4, 'chassis')
    )
    car = models.ForeignKey(Car, on_delete=models.CASCADE, to_field='uid')
    uid = models.CharField(max_length=10, unique=True)
    type = models.IntegerField(choices=COMPONENTS, default=0)


class Trip(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, to_field='uid')
    distance = models.IntegerField()
    start_date = models.DateTimeField(default=datetime.now, null=True)
    end_date = models.DateTimeField(default=datetime.now, null=True)
