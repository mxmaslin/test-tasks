from rest_framework import viewsets

from .models import Car, Component, Trip
from .serializers import CarSerializer, ComponentSerializer, TripSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer

    
class TripViewSet(viewsets.ModelViewSet):
    queryset = TripSerializer.objects.all()
    serializer_class = TripSerializer
