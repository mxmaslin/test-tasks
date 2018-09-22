import uuid

from datetime import datetime

from django.db import models


class Car(models.Model):
    uid = models.UUIDField(editable=False, unique=True)
    color = models.CharField(max_length=20)
    vendor = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    engine_identifier = models.CharField(max_length=20, unique=True)
    mileage = models.IntegerField()

    class Meta:
        ordering = ('vendor', 'model')

    def __str__(self):
        return f'{self.vendor} {self.model}, mileage: {self.mileage}'


class Component(models.Model):
    COMPONENTS = (
        (0, 'engine'),
        (1, 'body'),
        (2, 'electrical'),
        (4, 'chassis')
    )
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    uid = models.UUIDField(editable=False, unique=True)
    type = models.IntegerField(choices=COMPONENTS, default=0)

    class Meta:
        ordering = ('car', 'type')

    def __str__(self):
        return f'{self.car} {self.type}'


class Trip(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    distance = models.IntegerField()
    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ('start_date', 'end_date', 'distance')

    def __str__(self):
        return f'{self.start_date} {self.end_date}, {self.distance} miles'
