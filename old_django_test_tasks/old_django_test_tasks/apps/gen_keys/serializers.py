from rest_framework import serializers

from .models import Key


class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = '__all__'


class KeyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = ('value', )


class KeyExpireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = ('is_expired', )