from django.contrib.auth.models import User
from django.db import models


class Cat(models.Model):
    FLUFFINESS = (
        (0, 'No fur'),
        (1, 'Short-haired'),
        (2, 'Medium-haired'),
        (4, 'Fluffy')
    )
    fluffiness = models.IntegerField(choices=FLUFFINESS, default=2)
    name = models.CharField(max_length=10)
    age = models.IntegerField()
    breed = models.CharField(max_length=20)
    breeder = models.ForeignKey(User, on_delete=models.CASCADE)
