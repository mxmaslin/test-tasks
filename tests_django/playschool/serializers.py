from rest_framework import serializers

from .models import Scholar, Record


class ScholarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Scholar
        fields = '__all__'


class RecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Record
        fields = '__all__'
