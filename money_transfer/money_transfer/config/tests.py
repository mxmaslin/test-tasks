import os
from os.path import join

from .common import Common

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Tests(Common):
    ENVIRONMENT = 'Tests'

    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

    MEDIA_ROOT = join(os.path.dirname(BASE_DIR), 'test_media')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': 'localhost',
            'PORT': '5432',
            'NAME': 'money_transfer_test',
            'USER': 'money_transfer_test',
            'PASSWORD': 'money_transfer_test',
        }
    }

    MIDDLEWARE = (
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
    )
