from django.contrib import admin

from django.contrib import admin

from .models import Key


@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    list_display = ('value', 'is_provided', 'is_expired')
