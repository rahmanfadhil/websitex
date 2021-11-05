import functools

from django.shortcuts import redirect

from apps.users.utils import get_login_redirect_url


def only_unauthenticated(view_func):
    """
    Decorator for views that checks that the user is not authenticated, and
    redirects to `LOGIN_REDIRECT_URL` or `next` query string if authenticated.
    """

    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(get_login_redirect_url(request))
        return view_func(request, *args, **kwargs)

    return wrapper
