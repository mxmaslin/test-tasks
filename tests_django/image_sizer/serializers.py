# -*- coding: utf-8 -*-
import imghdr

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
        Убедимся, что у нас есть либо file, либо download_url
        """
        if 'file' in data or 'download_url' in data:
            pass
        else:
            raise serializers.ValidationError('No file nor url for file download')
        return data


class ResizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resize
        fields = '__all__'
