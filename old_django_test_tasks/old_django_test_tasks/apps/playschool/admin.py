from django.contrib import admin

from .models import Scholar, Record


@admin.register(Scholar)
class ScholarAdmin(admin.ModelAdmin):
    pass


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    pass