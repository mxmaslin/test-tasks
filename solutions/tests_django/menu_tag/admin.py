# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms

from .models import Menu, MenuItem


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass


class MenuAdminForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # мы не хотим, чтобы в админке пункт меню можно было указать собственным родителем
        super(MenuAdminForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = self.fields['parent'].queryset.exclude(pk=self.instance.pk)


@admin.register(MenuItem)
class MenuAdmin(admin.ModelAdmin):
    form = MenuAdminForm
    pass
