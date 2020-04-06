from django.db import models


class Key(models.Model):
    value = models.CharField(max_length=4, unique=True)
    is_provided = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return 'Value: {}, is_provided: {}, is_expired: {}'.format(
            self.value, self.is_provided, self.is_expired
        )

