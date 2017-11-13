# -*- coding: utf-8 -*-
from django.db import models

from rest_framework import serializers

from .models import (
    Application,
    Questionnaire,
    Submission)


class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = (
            'pk',
            'created',
            'modified',
            'rotation_started',
            'rotation_ended',
            'application_name',
            'application_type',
            'score_min',
            'score_max',
            #'bank',
        )


class QuestionnaireSerializer(serializers.ModelSerializer):

    class Meta:
        model = Questionnaire
        fields = (
            'pk',
            'created',
            'modified',
            'name',
            'birthday',
            'phone',
            'passport',
            'score',
        )


class SubmissionSerializer(serializers.ModelSerializer):

    # application = ApplicationSerializer(read_only=True)
    # questionnaire = QuestionnaireSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = (
            'pk',
            'created',
            'submitted',
            'application',
            'questionnaire',
            'status',
        )
