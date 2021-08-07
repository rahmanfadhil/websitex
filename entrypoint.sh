#!/bin/sh

set -e

python manage.py collectstatic --no-input
gunicorn config.wsgi:application --bind 0.0.0.0:8000
