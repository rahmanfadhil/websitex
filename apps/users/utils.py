from django.conf import settings
from django.http.request import HttpRequest
from django.shortcuts import resolve_url
from sesame.utils import get_query_string
from django.contrib.sites.models import Site

from apps.users.models import User
from apps.core.utils import send_html_email


def get_login_redirect_url(request: HttpRequest) -> str:
    """
    Returns an absolute URL to redirect to after the user logs in.
    """
    url = request.GET.get("next", settings.LOGIN_REDIRECT_URL)
    return request.build_absolute_uri(resolve_url(url))


def send_user_login_link(user: User, url: str):
    """
    Sends a login link to the user's email address.

    :param url: The absolute URL to redirect to after login
    """
    current_site = Site.objects.get_current()
    send_html_email(
        subject="Log in to " + current_site.name,
        to=[user.email],
        template_name="users/emails/login.html",
        context={"url": url + get_query_string(user), "user": user},
    )
