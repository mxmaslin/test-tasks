# -*- coding: utf-8 -*-
from django.db import models

from collections import OrderedDict


class Menu(models.Model):
    title = models.CharField(
        verbose_name='Название меню',
        max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    title = models.CharField(
        verbose_name='Название пункта меню',
        max_length=50)
    slug = models.SlugField(unique=True)
    menu = models.ForeignKey(Menu, related_name='menu_items')
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='children')

    class Meta:
        verbose_name = 'Элемент меню'
        verbose_name_plural = 'Элементы меню'
        ordering = ['slug']

    def __str__(self):
        return self.title
