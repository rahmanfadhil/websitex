from apps.pages.views import design, home
from django.urls import path

app_name = "pages"

urlpatterns = [
    path("", home, name="home"),
    path("design/", design, name="design"),
]
