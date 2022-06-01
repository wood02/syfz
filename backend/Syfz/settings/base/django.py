"""
Django settings for Syfz project.

Generated by 'django-admin startproject' using Django 3.1.13.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import sys
from pathlib import Path

from Syfz.settings.config import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f2frra)qnc286o_i6pg(!wmm5dfl&zmpk7#pt=g_7n=%hm-fg+'

# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv("DOCKERIZED"):
    DEBUG = True if os.getenv("DEBUG") == "1" else False
else:
    DEBUG = True if config.get('SYSTEM', "DEBUG") == 'True' else False
VERSION = config.get('SYSTEM', "VERSION") if config.get('SYSTEM', "VERSION") else "v1.0.1"

ALLOWED_HOSTS = ["*"]

ROOT_URLCONF = 'Syfz.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'django.template.context_processors.media',

            ],
        },
    },
]

WSGI_APPLICATION = 'Syfz.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace("\\", "/")

# 当APPEND_SLASH为True时，http://127.0.0.1:8000/users/1可以访问，
# 为False时，必须在1后面加一个 /

APPEND_SLASH = True
# APPEND_SLASH=False

# 日志级别
LOG_LEVEL = config.get("LOG", "LOG_LEVEL")

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
STATIC_ROOT = os.path.join(BASE_DIR, '/static/').replace("\\", "/")

AUTH_USER_MODEL = 'user.User'

# STATIC_ROOT = "...../static" # 静态文件存储路径 同时注释 STATICFILES_DIRS
