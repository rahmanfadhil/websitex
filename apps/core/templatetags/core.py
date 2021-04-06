from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def full_url(context, url):
    """
    Build a full url with domain and scheme (http or https).
    """
    return context.request.build_absolute_uri(url)
