from rest_framework import serializers

from .models import Image, Resize


class ImageSerializer(serializers.ModelSerializer):
    links = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='size-detail')

    class Meta:
        model = Image
        fields = ('name',
                  'created',
                  'file',
                  'download_url',
                  'format',
                  'jpeg_quality',
                  'links')


class ResizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resize
        field = ('width',
                 'height',
                 'download_url',
                 'image')
