from django.conf import settings
from django.contrib.messages.api import get_messages


def default_meta_tags(request):
    return {
        "PAGE_TITLE": settings.PAGE_TITLE,
        "DEFAULT_META_DESCRIPTION": settings.DEFAULT_META_DESCRIPTION,
        "DEFAULT_META_KEYWORDS": settings.DEFAULT_META_KEYWORDS,
        "DEFAULT_META_AUTHOR": settings.DEFAULT_META_AUTHOR,
    }


def json_messages(request):
    """Convert messages data to a JSON serializable format."""
    return {
        "json_messages": list(
            map(lambda x: {"message": str(x), "type": x.tags}, get_messages(request))
        )
    }
