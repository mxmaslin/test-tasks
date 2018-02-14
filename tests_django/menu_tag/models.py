# -*- coding: utf-8 -*-
import itertools
from unidecode import unidecode

from django.db import models
from django.template.defaultfilters import slugify

MAX_SLUG_LEN = 50


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
        self.slug = slugify(unidecode(self.title))[:MAX_SLUG_LEN]
        for x in itertools.count(1):
            if not Menu.objects.filter(slug=self.slug).exists():
                break
            self.slug = "%s-%d" % (self.slug[:MAX_SLUG_LEN - len(str(x)) - 1], x)
        print(self.slug)
        super(Menu, self).save(*args, **kwargs)


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
        self.slug = slugify(unidecode(self.title))[:MAX_SLUG_LEN]
        for x in itertools.count(1):
            if not MenuItem.objects.filter(slug=self.slug).exists():
                break
            self.slug = "%s-%d" % (self.slug[:MAX_SLUG_LEN - len(str(x)) - 1], x)
        print(self.slug)
        super(MenuItem, self).save(*args, **kwargs)
