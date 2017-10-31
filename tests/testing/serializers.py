# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import User
from .models import QuestionSet
from .models import Question
from .models import Option
from .models import Submission


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
                    'name',
                    'role',
                    'question_set')


class QuestionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionSet
        fields = (
                    'author',
                    'name',
                    'created')


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
                    'question',
                    'ordering',
                    'question_sets')


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
                    'question',
                    'value',
                    'ordering',
                    'is_correct')


class SubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submission
        fields = (
                    'respondent',
                    'option')
