# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms

from .models import Menu, MenuItem


class MenuItemInLine(admin.TabularInline):
    model = MenuItem
    exclude = ('slug', )


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        exclude = ('slug', )

    def __init__(self, *args, **kwargs):
        # мы не хотим, чтобы в админке пункт меню можно было указать собственным родителем
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = self.fields['parent'].queryset.exclude(pk=self.instance.pk)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    form = MenuItemForm

    list_display = (
        'title',
        'menu',
        'parent')
    exclude = ('slug', )


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('title',)
    exclude = ('slug', )
    inlines = (MenuItemInLine, )
