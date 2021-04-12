from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def full_url(context, url):
    """
    Build a full url with domain and scheme (http or https).
    """
    return (
        context.request.build_absolute_uri(url) if hasattr(context, "context") else url
    )


@register.simple_tag(takes_context=True)
def active_link(context, url_name):
    """
    Returns nav link active class if the current page is active.
    """
    return (
        "active"
        if hasattr(context, "context")
        and context.request.resolver_match.url_name == url_name
        else ""
    )
