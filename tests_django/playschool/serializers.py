import base64
import imghdr
import six
import uuid

from django.core.files.base import ContentFile

from rest_framework import serializers

from .models import Scholar, Record


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super().to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        return extension


# class ScholarSerializer(serializers.ModelSerializer):
#     photo = Base64ImageField(max_length=None, use_url=True)
#
#     class Meta:
#         model = Scholar
#         fields = ('photo',
#                   'name',
#                   'sex',
#                   'birth_date',
#                   'school_class',
#                   'is_studying')


class ScholarSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(
        required=False,
        max_length=None,
        allow_empty_file=True,
        use_url=True)

    class Meta:
        model = Scholar
        fields = (
            'pk',
            'photo',
            'name',
            'sex',
            'birth_date',
            'school_class',
            'is_studying')


class RecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Record
        fields = (
            'pk',
            'scholar',
            'date',
            'has_came_with',
            'time_arrived',
            'time_departed'
        )
