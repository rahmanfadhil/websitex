import os

from django import template
from django.forms.boundfield import BoundField
from django.urls import resolve
from django.urls.exceptions import Resolver404

register = template.Library()


@register.simple_tag(takes_context=True)
def full_url(context, url) -> str:
    """
    Build a full url with domain and scheme (http or https).
    """
    if hasattr(context, "request"):
        return context.request.build_absolute_uri(url)
    return url


@register.simple_tag(takes_context=True)
def is_link_active(context, *view_names) -> bool:
    """
    Returns a boolean indicating if the nav link is the current page.
    """

    if hasattr(context, "request"):
        try:
            match = resolve(context.request.path_info)
            if match.view_name in view_names:
                return True
        except Resolver404:
            return False

    return False


@register.simple_tag
def form_field(field: BoundField, **kwargs) -> str:
    """
    Render a form field with additional HTML attributes.
    """
    return field.as_widget(attrs=kwargs)


@register.filter
def file_name(file_path: str) -> str:
    """
    Get the file name from a file path.
    """
    return os.path.basename(file_path)
