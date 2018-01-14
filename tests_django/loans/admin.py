from django.contrib import admin

from .models import (
    Application,
    Questionnaire,
    Submission)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = (
        'application_name',
        'application_type',
        'score_min',
        'score_max',
        'created',
        'modified',
        'rotation_started',
        'rotation_ended'
        )

    search_fields = (
        'application_name',)

    list_filter = (
        'created',
        'application_type',
        'score_min',
        'score_max')


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'birthday',
        'phone',
        'passport',
        'score',
        'created',
        'modified'
        )

    search_fields = (
        'name',
        'phone',
        'passport')

    list_filter = (
        'birthday',
        'created',
        'score')


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):

    list_display = (
        'application',
        'questionnaire',
        'status',
        'created',
        'submitted'
        )

    search_fields = (
        'application',
        'questionnaire')

    list_filter = (
        'application',
        'questionnaire',
        'status',
        'created')
