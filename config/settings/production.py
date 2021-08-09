from .base import *


# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# DJANGO-ANYMAIL CONFIG
# ------------------------------------------------------------------------------
# https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
INSTALLED_APPS += ["anymail"]
# https://anymail.readthedocs.io/en/stable/esps/amazon_ses/#installation
EMAIL_BACKEND = "anymail.backends.amazon_ses.EmailBackend"

# SECURITY
# ------------------------------------------------------------------------------
if os.environ.get("USE_HTTPS", "False").lower() == "true":
    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
    SECURE_SSL_REDIRECT = True
    # https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
    SESSION_COOKIE_SECURE = True
    # https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
    CSRF_COOKIE_SECURE = True
    # https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
    SECURE_HSTS_SECONDS = os.environ.get("DJANGO_SECURE_HSTS_SECONDS", 60)
    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
    SECURE_HSTS_INCLUDE_SUBDOMAINS = (
        os.environ.get("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", "True").lower()
        == "true"
    )
    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
    SECURE_HSTS_PRELOAD = (
        os.environ.get("DJANGO_SECURE_HSTS_PRELOAD", "False").lower() == "true"
    )

# DJANGO-STORAGES
# ------------------------------------------------------------------------------
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
AWS_S3_FILE_OVERWRITE = False

# LOGGING
# ------------------------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}

# CELERY
# ------------------------------------------------------------------------------
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#broker-use-ssl
CELERY_BROKER_USE_SSL = True
