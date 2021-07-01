from django.conf import settings
from django.contrib.messages.api import get_messages
from django.http import HttpRequest
from django.urls.base import resolve


def default_meta_tags(request: HttpRequest):
    """
    Provides the default meta tags for SEO.
    """
    return {
        "PAGE_TITLE": settings.PAGE_TITLE,
        "DEFAULT_META_DESCRIPTION": settings.DEFAULT_META_DESCRIPTION,
        "DEFAULT_META_KEYWORDS": settings.DEFAULT_META_KEYWORDS,
        "DEFAULT_META_AUTHOR": settings.DEFAULT_META_AUTHOR,
    }


def page_data(request: HttpRequest):
    """
    Provides a JSON data for JavaScript to show notifications from Django
    messages framework, get the current view name, etc.
    """
    messages = map(lambda x: {"message": str(x), "type": x.tags}, get_messages(request))
    return {
        "page_data": {
            "messages": list(messages),
            "view_name": resolve(request.path_info).view_name,
        }
    }
