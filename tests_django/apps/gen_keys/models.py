from django.db import models


class Key(models.Model):
    value = models.CharField(max_length=4, unique=True)
    is_provided = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)

