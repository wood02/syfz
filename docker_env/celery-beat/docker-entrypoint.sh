#!/bin/sh

cd /code
python ./manage.py makemigrations
python ./manage.py migrate
#celery -A Syfz beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --logfile=logs/celery-beat.log
celery -A Syfz beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
#exec "$@"
