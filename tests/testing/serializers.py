# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Question
from .models import Answer
from .models import Test
from .models import Author
from .models import Respondent


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
                    'question',
                    'ordering',
                    'tests')


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = (
                    'answer',
                    'question',
                    'ordering',
                    'is_correct')


class TestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        fields = (
                    'author',
                    'created')


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = (
                    'name',)


class RespondentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Respondent
        fields = (
                    'name',
                    'tests')
