from django.conf import settings


def default_meta_tags(request):
    return {
        "PAGE_TITLE": settings.PAGE_TITLE,
        "DEFAULT_META_DESCRIPTION": settings.DEFAULT_META_DESCRIPTION,
        "DEFAULT_META_KEYWORDS": settings.DEFAULT_META_KEYWORDS,
        "DEFAULT_META_AUTHOR": settings.DEFAULT_META_AUTHOR,
    }
