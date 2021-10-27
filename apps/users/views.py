from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views.decorators.http import require_http_methods, require_POST
from sesame.utils import get_query_string

from apps.users.forms import EmailLoginForm, UserUpdateForm
from apps.users.models import User


@require_POST
@login_required
def logout(request: HttpRequest) -> HttpResponse:
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("pages:home")


@require_http_methods(["GET", "POST"])
def login(request: HttpRequest) -> HttpResponse:
    form = EmailLoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user, _ = User.objects.get_or_create(email=form.cleaned_data["email"])

        next_url = request.GET.get("next", reverse("pages:home"))
        url = request.build_absolute_uri(next_url + get_query_string(user))
        user.send_login_link(url)

        messages.success(request, "We have sent you an email with a link to login.")
        return redirect("pages:home")
    else:
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
        messages.success(request, "Your profile has been updated.")
        return redirect("users:update_user")
    else:
        return render(request, "users/update_user.html", {"form": form})


@require_POST
@login_required
def delete_user(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        request.user.delete()
        messages.success(request, "Your account has been deleted.")
    return redirect("pages:home")
