# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
import os
from Syfz.settings.config import config

if os.getenv("DOCKERIZED"):
    DATABASES = {
        'default': {
            # 'ENGINE': 'django.db.backends.mysql',
            'ENGINE': 'dj_db_conn_pool.backends.mysql',  # 连接池
            'NAME': os.getenv("MYSQL_DATABASE"),
            'USER':  os.getenv("MYSQL_USER"),
            'PASSWORD': os.getenv("MYSQL_ROOT_PASSWORD"),
            'HOST': os.getenv("MYSQL_HOST"),
            'PORT': os.getenv("MYSQL_PORT"),
            # 'ATOMIC_REQUESTS': True,
            'OPTIONS': {'charset': 'utf8mb4'},
            # 连接池
            'POOL_OPTIONS': {
                'POOL_SIZE': 10,
                'MAX_OVERFLOW': 10
            }
        },

    }

    # redis
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://:AREprNahAZwZDLy6@redis:6379/5",  # 这里设定了本机的redis数据
            # "LOCATION": "redis://:Admin2021@@47.193.146.xxx:6379/0",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }
else:

    DATABASES = {
        'default': {
            # 'ENGINE': 'django.db.backends.mysql',
            'ENGINE': 'dj_db_conn_pool.backends.mysql',  # 连接池
            'NAME': config.get('mysql', 'DB_NAME'),
            'USER': config.get('mysql', 'DB_USER'),
            'PASSWORD': config.get('mysql', 'DB_PASSWORD'),  # AREprNahAZwZDLy6
            'HOST': config.get('mysql', 'DB_HOST'),
            'PORT': config.get('mysql', 'DB_PORT'),
            # 'ATOMIC_REQUESTS': True,
            'OPTIONS': {'charset': 'utf8mb4'},
            # 连接池
            'POOL_OPTIONS': {
                'POOL_SIZE': 10,
                'MAX_OVERFLOW': 10
            }
        },

    }

    # redis
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/5",  # 这里设定了本机的redis数据
            # "LOCATION": "redis://:Admin2021@@47.193.146.xxx:6379/0",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }
