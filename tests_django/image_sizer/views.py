# -*- coding: utf-8 -*-
from django.urls import resolve

from django.http import Http404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Image, Resize
from .serializers import ImageSerializer, ResizeSerializer


@api_view(['POST'])
def image_create(request):
    """
    http POST http://127.0.0.1:8000/image-sizer/ <<< '{"file": "test", "download": "http://image.com/image.jpg", "resizes": [{"width": 100, "height": 150, "format": "jpg", "jpg_quality": 80}, {"width": 100, "height": 150}]}'
    """
    serializer = ImageSerializer(data=request.data)
    if serializer.is_valid():
        if 'file' in request.data:
            print('got file and maybe url')
            pass
        else:
            print('no file, got url')
            pass



        serializer.save()

        image = Image.ob
        # for i in Image.objects.all():
        #     #13
        #     print(i.pk)
        #     print(i.file)
        #     print(resolve('http://127.0.0.1:8000/image-sizer/' + i.file.url))

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResizeDetail(APIView):
    def get_object(self, resize_url):
        try:
            pk = resolve(resize_url).kwargs['pk']
            return Resize.objects.get(pk)
        except Resize.DoesNotExist:
            raise Http404

    def get(self, request, resize_url, format=None):
        resize = self.get_object(resize_url)
        serializer = ResizeSerializer(resize)
        return Response(serializer.data)

    def delete(self, request, resize_url, format=None):
        resize = self.get_object(resize_url)
        resize.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
