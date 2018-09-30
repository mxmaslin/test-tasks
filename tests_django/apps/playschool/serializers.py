import base64
import imghdr
import six
import uuid

from django.core.files.base import ContentFile

from rest_framework import serializers

from .models import Scholar, Record


class ScholarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Scholar
        fields = (
            'pk',
            'photo',
            'name',
            'sex',
            'birth_date',
            'school_class',
            'is_studying')


class RecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Record
        fields = (
            'pk',
            'scholar',
            'date',
            'has_came_with',
            'time_arrived',
            'time_departed'
        )
