from configurations import Configuration
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Common(Configuration):
    SECRET_KEY = 'django-insecure-q_&8d1@nx1m13ywxp1%evlw%vylzx^xl_qv1sre3hefc06qa#6'
    ENVIRONMENT = 'Common'
    APP_NAME = 'money_transfer'
    DEBUG = True
    ALLOWED_HOSTS = []

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'djmoney',
        'rest_framework',
        'main.apps.MainConfig',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    ROOT_URLCONF = 'money_transfer.urls'
    WSGI_APPLICATION = 'money_transfer.wsgi.application'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'money_transfer',
            'USER': 'money_transfer',
            'PASSWORD': 'money_transfer',
            'HOST': 'localhost',
            'PORT': 5432,
        }
    }

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    LANGUAGE_CODE = 'ru'
    TIME_ZONE = 'Europe/Moscow'
    USE_I18N = True
    USE_TZ = True
    STATIC_URL = 'static/'
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
