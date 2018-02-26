from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    list_display = ('user', 'inn', 'balance')

    search_fields = ('user', 'inn')

    list_filter = ('user', 'inn')
