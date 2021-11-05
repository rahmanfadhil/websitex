from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods, require_POST

from apps.users.decorators import only_unauthenticated
from apps.users.forms import LoginForm, SignupForm, UserUpdateForm
from apps.users.models import User
from apps.users.utils import get_login_redirect_url, send_user_login_link


@require_POST
@login_required
def logout(request: HttpRequest) -> HttpResponse:
    auth_logout(request)
    messages.success(request, _("You have been logged out."))
    return redirect("pages:home")


@only_unauthenticated
@require_http_methods(["GET", "POST"])
def signup(request: HttpRequest) -> HttpResponse:
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        send_user_login_link(user, get_login_redirect_url(request))
        messages.success(request, _("We have sent you an email with a link to login."))
        return redirect("pages:home")
    return render(request, "users/signup.html", {"form": form})


@only_unauthenticated
@require_http_methods(["GET", "POST"])
def login(request: HttpRequest) -> HttpResponse:
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            user = User.objects.get(email=form.cleaned_data["email"])
            send_user_login_link(user, get_login_redirect_url(request))
            messages.success(
                request, _("We have sent you an email with a link to login.")
            )
            return redirect("pages:home")
        except User.DoesNotExist:
            form.add_error("email", "This email is not registered.")
    return render(request, "users/login.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def update_user(request: HttpRequest) -> HttpResponse:
    form = UserUpdateForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user,
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Your profile has been updated."))
        return redirect("users:update_user")
    else:
        return render(request, "users/update_user.html", {"form": form})


@require_POST
@login_required
def delete_user(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        request.user.delete()
        messages.success(request, _("Your account has been deleted."))
    return redirect("pages:home")
