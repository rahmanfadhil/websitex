from django.conf import settings
from django.contrib.messages.api import get_messages
from django.http import HttpRequest
from django.urls.base import resolve
from django.urls.exceptions import Resolver404


def default_page_title(request: HttpRequest):
    """
    Provides the default page title for every page
    """
    return {"DEFAULT_PAGE_TITLE": settings.DEFAULT_PAGE_TITLE}


def page_data(request: HttpRequest):
    """
    Provides a JSON data for JavaScript to show notifications from Django
    messages framework, get the current view name, etc.
    """
    messages = map(lambda x: {"message": str(x), "type": x.tags}, get_messages(request))
    return {
        "page_data": {
            "messages": list(messages),
            "view_name": request.resolver_match.view_name,
            "args": request.resolver_match.args,
            "kwargs": request.resolver_match.kwargs,
        }
    }
