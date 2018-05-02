from django.db import models


class Image(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/', null=True)
    download_url = models.URLField(null=True, unique=True)
    jpeg_quality = models.IntegerField(null=True)


class Resize(models.Model):
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    download_url = models.URLField(null=True, unique=True)
    image = models.ForeignKey(
        Image, related_name='resizes', on_delete=models.CASCADE)
