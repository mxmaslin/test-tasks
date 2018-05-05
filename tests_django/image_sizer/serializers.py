# -*- coding: utf-8 -*-
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
                  'file',
                  'download_url',
                  'jpeg_quality',
                  'links')

    def validate(self, data):
        """
        Убедимся, что у нас есть либо file, либо download_url
        """
        if not any([data['file'], data['download_url']]):
            raise serializers.ValidationError('No file nor url for file download')
        return data


class ResizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resize
        field = ('width',
                 'height',
                 'download_url',
                 'image')
