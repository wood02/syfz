#!/bin/sh

cd /code
python ./manage.py makemigrations
python ./manage.py migrate
uwsgi --ini uwsgi_docker.ini

#exec "$@"
