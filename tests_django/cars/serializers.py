from rest_framework import serializers

from .models import Car, Component, Trip


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ('pk',
                  'uid',
                  'car',
                  'type')


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ('pk',
                  'car',
                  'distance',
                  'start_date',
                  'end_date')


class CarSerializer(serializers.ModelSerializer):
    trip_set = TripSerializer(read_only=True, many=True)
    component_set = ComponentSerializer(read_only=True, many=True)

    class Meta:
        model = Car
        fields = ('pk',
                  'uid',
                  'color',
                  'vendor',
                  'model',
                  'engine_identifier',
                  'mileage',
                  'trip_set',
                  'component_set')
