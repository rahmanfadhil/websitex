from django import template
from django.urls import resolve

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
def active_link(context, *view_names) -> str:
    """
    Returns nav link active class if the current page is active.
    """
    if is_link_active(context, *view_names):
        return "active"
    return ""


@register.simple_tag(takes_context=True)
def is_link_active(context, *view_names) -> bool:
    """
    Returns a boolean indicating if the nav link is the current page.
    """

    if hasattr(context, "request"):
        for view_name in view_names:
            try:
                match = resolve(context.request.path_info)
                if match.view_name == view_name:
                    return True
            except:
                pass
    return False


@register.inclusion_tag("core/icon.html")
def icon(name, css_class=None):
    """
    Renders a feather icon.
    """
    return {"name": name, "css_class": css_class}
