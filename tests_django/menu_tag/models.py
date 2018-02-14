# -*- coding: utf-8 -*-
import itertools
from unidecode import unidecode

from django.db import models
from django.template.defaultfilters import slugify


class Menu(models.Model):
    title = models.CharField(
        verbose_name='Название меню',
        max_length=50)
    slug = models.SlugField()

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        max_slug_len = 49
        if not self.pk:
            slug = slugify(unidecode(self.title[:max_slug_len]))
            print(slug)
            for x in itertools.count(1):
                if not Menu.objects.filter(
                        title=self.title,
                        slug=self.slug).exists():
                    break
                trailing_number_len = len(str(x))
                slug = self.slug[:max_slug_len - trailing_number_len]
                slug = '{slug}-{x}'.format(slug, x)
            self.slug = slug
        print(self.slug)
        super().save(*args, **kwargs)


class MenuItem(models.Model):
    title = models.CharField(
        verbose_name='Название пункта меню',
        max_length=50)
    slug = models.SlugField()
    menu = models.ForeignKey(
        Menu,
        related_name='menu_items',
        verbose_name='Меню',
        on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='children',
        verbose_name='Родитель',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Элемент меню'
        verbose_name_plural = 'Элементы меню'
        ordering = ['slug']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        max_slug_len = 49
        if not self.pk:
            slug = slugify(unidecode(self.title[:max_slug_len]))
            for x in itertools.count(1):
                if not MenuItem.objects.filter(
                        title=self.title,
                        slug=self.slug).exists():
                    break
                trailing_number_len = len(str(x))
                slug = self.slug[:max_slug_len - trailing_number_len]
                slug = '{slug}-{x}'.format(slug, x)
            self.slug = slug
        super().save(*args, **kwargs)
