from django.db import IntegrityError
from django.http import Http404
from django.utils.crypto import get_random_string

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Key
from .serializers import KeySerializer, KeyCreateSerializer, KeyExpireSerializer


def generate_value(length=4):
    return get_random_string(length)


@api_view(['GET'])
def provide_key(request):
    provide_key = Key.objects.filter(is_provided=False).first()
    provide_key.is_provided = True
    provide_key.save()
    serializer = KeySerializer(provide_key)
    return Response(serializer.data, status.HTTP_200_OK)


class KeyList(APIView):
    def get(self, request, format=None):
        not_provided_count = Key.objects.filter(is_provided=False).count()
        return Response({'not_provided': not_provided_count})

    def post(self, request, format=None):
        max_attempts = 4
        while True:
            value = generate_value()
            serializer = KeyCreateSerializer(data={'value': value})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                max_attempts -= 1
                if max_attempts == 0:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KeyDetail(APIView):
    def get_object(self, pk):
        try:
            return Key.objects.get(pk=pk)
        except Key.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        key = self.get_object(pk)
        serializer = KeySerializer(key)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        key = self.get_object(pk)
        if key.is_expired:
            return Response({'error': 'The key was expired already'},
                            status=status.HTTP_400_BAD_REQUEST
                            )
        if not key.is_provided:
            return Response({'error': 'The key must be provided first'},
                            status=status.HTTP_400_BAD_REQUEST
                            )
        key.is_expired = True
        serializer = KeyExpireSerializer(key, data={})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
