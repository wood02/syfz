#!/bin/sh

cd /code
python ./manage.py makemigrations
python ./manage.py migrate

exec "$@"
