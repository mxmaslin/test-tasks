from django.db import models
from django.urls import reverse
from slugify import slugify


from ckeditor.fields import RichTextField


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    content = RichTextField()
    image = models.ImageField(upload_to=f'blog/images/%Y/%m/%d')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        print("yay " * 1000)
        print(reverse('blog:post_detail', args=[self.slug]))
        return reverse('blog:post_detail', args=[self.slug])


