from django.urls import path

from apps.pages.views import home


app_name = "pages"

urlpatterns = [
    path("", home, name="home"),
]
