# -*- coding: utf-8 -*-
# Application definition

INSTALLED_APPS = [
    "simpleui",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'djoser',
    'django_filters',
    'corsheaders',
    # 'easyaudit',
    'django_celery_results',
    # 'haystack',
    'drf_yasg',
    'django_celery_beat',

    # app
    'apps.alarm',
    'apps.user',
    'apps.system',
    'apps.tracesource',
    'apps.plugins',
    'apps.poc',
]



