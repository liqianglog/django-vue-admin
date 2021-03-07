#!/bin/bash

cd /dvadmin-backend

python ./manage.py makemigrations
python ./manage.py migrate
#python ./manage.py initialization
#python ./manage.py runserver 0.0.0.0:8000
uwsgi --ini azcrm/uwsgi.ini
#if [[ $ENV == "preprod" ]] || [[ $ENV == "prod" ]]; then
#    uwsgi --ini azcrm/uwsgi.ini
#else
#    python ./manage.py runserver 0.0.0.0:8000
#fi
