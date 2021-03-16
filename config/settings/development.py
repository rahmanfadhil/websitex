from .base import *
import socket


# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/topics/files/
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

# DJANGO-DEBUG-TOOLBAR CONFIGS
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#configuring-internal-ips
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#enabling-middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
