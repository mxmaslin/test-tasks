from rest_framework import serializers

from .models import Application
from .models import Questionnaire
from .models import Submission


class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = (
            'pk',
            'created',
            'modified',
            'rotation_started',
            'rotation_ended',
            'applicaton_name',
            'application_type',
            'score_min',
            'score_max',
            'bank',
        )


class QuestionnaireSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Questionnaire
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

    class Meta:
        model = models.Submission
        fields = (
            'pk',
            'created',
            'submitted',
            'questionnaire',
            'application',
            'status',
        )
