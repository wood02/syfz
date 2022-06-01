#!/bin/sh

cd /code
python ./manage.py makemigrations
python ./manage.py migrate
#celery -A Syfz.celery_main  worker -l info --logfile=logs/celery-worker.log
celery -A Syfz.celery_main  worker -l info
#exec "$@"
