from rest_framework import serializers

from .models import Image, Size


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


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        field = ('width',
                 'height',
                 'link',
                 'image')
