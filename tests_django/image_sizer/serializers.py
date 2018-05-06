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
        fields = ('name',
                  'file',
                  'download_url',
                  'jpeg_quality',
                  'resizes')

    def validate(self, data):
        """
        Убедимся, что у нас есть либо file, либо download_url
        """
        file = True
        download_url = True
        try:
            data['file']
        except KeyError:
            file = False
        try:
            data['download_url']
        except KeyError:
            download_url = False
        if not any([file, download_url]):
            raise serializers.ValidationError('No file nor url for file download')
        return data

    def validate_file(self, data):
        """
        Убедимся, что file является изображением поддерживаемого типа
        """
        try:
            data['file']
        except KeyError:
            pass
        else:
            if imghdr.what not in ('png', 'gif', 'jpg'):
                raise serializers.ValidationError('Unsupported file format')
        return data


class ResizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resize
        fields = ('width',
                  'height',
                  'download_url',
                  'image')
