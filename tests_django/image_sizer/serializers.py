# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Image, Resize


class ImageSerializer(serializers.ModelSerializer):

    resizes = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='resize-detail')

    class Meta:
        model = Image
        fields = '__all__'

    def validate(self, data):
        """
        Убедимся, что у нас есть либо file, либо download
        """
        if 'file' in data or 'download' in data:
            pass
        else:
            raise serializers.ValidationError('No file nor url for file download')
        return data


class ResizeSerializer(serializers.ModelSerializer):

    resize_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Resize
        fields = ('width',
                  'height',
                  'image',
                  'resize_file',
                  'resize_file_url')

    def get_resize_file_url(self, obj):
        return obj.resize_file.url
