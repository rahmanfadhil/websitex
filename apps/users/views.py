from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods, require_POST

from apps.users.forms import SignupForm, UserUpdateForm


@require_http_methods(["GET", "POST"])
def signup(request: HttpRequest) -> HttpResponse:
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        auth_login(request, user)
        messages.success(request, _("Your account has been created."))
        return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "users/signup.html", {"form": form})


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
    return render(request, "users/update_user.html", {"form": form})


@require_POST
@login_required
def delete_user(request: HttpRequest) -> HttpResponse:
    request.user.delete()
    messages.success(request, _("Your account has been deleted."))
    return redirect("pages:home")


password_reset = PasswordResetView.as_view(
    html_email_template_name="users/password_reset_email.html"
)
