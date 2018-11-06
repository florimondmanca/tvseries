#!/usr/bin/env bash

# Wait for DB container to be up
sleep 3s
# Run migrations and then the production server
python manage.py migrate --noinput
exec gunicorn uptv.wsgi -c python:uptv.gunicorn
