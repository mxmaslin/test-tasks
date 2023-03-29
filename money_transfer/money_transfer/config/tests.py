import os
from dotenv import load_dotenv
from os.path import join
from pathlib import Path

from .common import Common


env_path = Path.cwd().joinpath('.env')
load_dotenv(env_path)

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
            'HOST': os.getenv('POSTGRES_HOST'),
            'PORT': os.getenv('POSTGRES_PORT'),
            'NAME': os.getenv('POSTGRES_DBNAME'),
            'USER': os.getenv('POSTGRES_USER'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        }
    }

    MIDDLEWARE = (
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
    )
