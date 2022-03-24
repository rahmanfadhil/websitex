from django.contrib.messages.api import get_messages
from django.http import HttpRequest


def page_data(request: HttpRequest):
    """
    Provides a JSON data for JavaScript to show notifications from Django
    messages framework, get the current view name, args, kwargs, etc.
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
