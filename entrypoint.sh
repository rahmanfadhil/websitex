#!/usr/bin/env bash

python manage.py collectstatic --no-input
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --log-level=debug
