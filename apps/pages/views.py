from django.shortcuts import render


def home(request):
    return render(request, "pages/home.html")


def design(request):
    return render(request, "pages/design.html")
