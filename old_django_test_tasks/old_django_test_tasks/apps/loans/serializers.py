# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import (
    Offer,
    Questionnaire,
    Submission)


class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = (
            'pk',
            'created',
            'modified',
            'rotation_started',
            'rotation_ended',
            'offer_name',
            'offer_type',
            'score_min',
            'score_max',
            'bank',
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

    offer = OfferSerializer(read_only=True)
    questionnaire = QuestionnaireSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = (
            'pk',
            'created',
            'submitted',
            'offer',
            'questionnaire',
            'status',
        )


class SubmissionSerializerPost(serializers.ModelSerializer):

    class Meta:
        model = Submission
        fields = (
            'pk',
            'created',
            'submitted',
            'offer',
            'questionnaire',
            'status',
        )
