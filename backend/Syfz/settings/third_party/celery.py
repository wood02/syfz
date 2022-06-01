# -*- coding: utf-8 -*-


from __future__ import absolute_import

import os

from django.conf import settings

# 设置代理人broker
CELERY_BROKER_URL = 'redis://:AREprNahAZwZDLy6@redis:6379/3' if os.getenv("DOCKERIZED") else 'redis://127.0.0.1:6379/3'

# 指定 Backend
CELERY_RESULT_BACKEND = 'redis://:AREprNahAZwZDLy6@redis:6379/4' if os.getenv(
    "DOCKERIZED") else 'redis://127.0.0.1:6379/4'  # redis
# CELERY_RESULT_BACKEND = 'django-db'  # 数据库
# 指定时区，默认是 UTC
# CELERY_TIMEZONE = settings.TIME_ZONE
CELERY_TIMEZONE = 'Asia/Shanghai'
# celery 序列化与反序列化配置

# celery内容等消息的格式设置，默认json
CELERY_ACCEPT_CONTENT = ['application/json', ]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# result_expires = 60 * 60 # 任务结果过期时间
CELERY_RESULT_EXPIRES = 60 * 60 * 3

# CELERY_IGNORE_RESULT = True
# celery 的启动工作数量设置
CELERY_WORKER_CONCURRENCY = 10

# 任务预取功能，会尽量多拿 n 个，以保证获取的通讯成本可以压缩。
CELERYD_PREFETCH_MULTIPLIER = 20

# 有些情况下可以防止死锁
CELERYD_FORCE_EXECV = True

# celery 的 worker 执行多少个任务后进行重启操作
CELERY_WORKER_MAX_TASKS_PER_CHILD = 100

# 禁用所有速度限制，如果网络资源有限，不建议开足马力。
CELERY_DISABLE_RATE_LIMITS = True

# celery beat配置（周期性任务设置）
# https://django-celery-beat.readthedocs.io/en/latest/index.html?highlight=import_contacts
CELERY_ENABLE_UTC = False
DJANGO_CELERY_BEAT_TZ_AWARE = False
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# https://django-celery-beat.readthedocs.io/en/latest/
# celery -A Syfz beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler #启动beta 调度器使用数据库 (定时任务)
# celery -A Syfz.celery_main  worker -l info -P eventlet
