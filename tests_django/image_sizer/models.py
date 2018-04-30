from django.db import models


class Image(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/', null=True)
    download_url = models.URLField(null=True)
    JPG = 'jpeg'
    GIF = 'gif'
    PNG = 'png'
    FORMAT_CHOICES = (
        (JPG, 'jpg'),
        (GIF, 'gif'),
        (PNG, 'png'),
    )
    format = models.CharField(
        max_length=3, choices=FORMAT_CHOICES, default=JPG)
    jpeg_quality = models.IntegerField(null=True)

    class Meta:
        ordering = ('name', 'created')


class Size(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()
    link = models.URLField(null=True)
    image = models.ForeignKey(
        Image, related_name='sizes', on_delete=models.CASCADE)
