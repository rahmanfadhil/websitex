from config.settings.base import *

# WHITENOISE
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/stable/django.html#whitenoise-makes-my-tests-run-slow
WHITENOISE_AUTOREFRESH = True

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/topics/files/
MEDIA_ROOT = "/tmp"
