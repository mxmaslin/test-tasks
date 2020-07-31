from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from ckeditor.fields import RichTextField


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    # content = RichTextField()
    content = models.TextField()
    image = models.ImageField(upload_to=f'blog_images/{slug}')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])


