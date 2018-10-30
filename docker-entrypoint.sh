#!/usr/bin/env bash

# Run migrations and then the production server
python manage.py migrate --noinput
exec gunicorn uptv.wsgi -c python:uptv.gunicorn
