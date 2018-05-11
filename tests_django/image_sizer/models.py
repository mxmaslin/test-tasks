from django.db import models


class Image(models.Model):
    file = models.ImageField(upload_to='uploads/', null=True)
    download_url = models.URLField(null=True)

    def __str__(self):
        return f'{self.file}'


class Resize(models.Model):
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    file = models.ImageField(upload_to='uploads/', null=True)
    image = models.ForeignKey(
        Image, related_name='resizes', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.image} {self.width}x{self.height}'
