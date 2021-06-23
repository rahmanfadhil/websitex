from config.settings.base import *


# Disable whitenoise
INSTALLED_APPS.remove("whitenoise.runserver_nostatic")
MIDDLEWARE.remove("whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"


# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/topics/files/
MEDIA_ROOT = "/tmp"
MEDIA_URL = "/media/"
