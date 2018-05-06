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
    http POST http://127.0.0.1:8000/image-sizer/ <<< '{"name": "shit", "download_url": "http://shit.com", "resizes": []}'
    """
    serializer = ImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResizeDetail(APIView):
    def get_object(self, download_url):
        try:
            return Resize.objects.get(download_url=download_url)
        except Resize.DoesNotExist:
            raise Http404

    def get(self, request, download_url, format=None):
        resize = self.get_object(download_url)
        serializer = ResizeSerializer(resize)
        return Response(serializer.data)

    def delete(self, request, download_url, format=None):
        resize = self.get_object(download_url)
        resize.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
