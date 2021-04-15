from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def full_url(context, url):
    """
    Build a full url with domain and scheme (http or https).
    """
    if hasattr(context, "request"):
        return context.request.build_absolute_uri(url)
    return url


@register.simple_tag(takes_context=True)
def active_link(context, *url_name):
    """
    Returns nav link active class if the current page is active.
    """
    if hasattr(context, "request"):
        if context.request.resolver_match.url_name in url_name:
            return "active"
    return ""
