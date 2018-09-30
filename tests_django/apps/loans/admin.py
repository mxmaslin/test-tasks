from django.contrib import admin

from .models import (
    Offer,
    Questionnaire,
    Submission)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):

    list_display = (
        'offer_name',
        'offer_type',
        'score_min',
        'score_max',
        'created',
        'modified',
        'rotation_started',
        'rotation_ended'
        )

    search_fields = ('offer_name',)

    list_filter = (
        'created',
        'offer_type',
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
        'offer',
        'questionnaire',
        'status',
        'created',
        'submitted'
        )

    search_fields = (
        'offer',
        'questionnaire')

    list_filter = (
        'offer',
        'questionnaire',
        'status',
        'created')
