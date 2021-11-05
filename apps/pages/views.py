from django import forms
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from apps.core.utils import client_redirect
from apps.core.widgets import TrixInput


class HomeForm(forms.Form):
    email = forms.EmailField()
    content = forms.CharField(widget=TrixInput)


@require_http_methods(["GET", "POST"])
def home(request):
    form = HomeForm(request.POST or None)
    context = {"form": form}
    if request.method == "POST":
        if form.is_valid():
            messages.success(request, "asdfasdfasdf")
            return client_redirect("users:login")
        else:
            return render(request, "pages/home_form.html", context)
    return render(request, "pages/home.html", context)
