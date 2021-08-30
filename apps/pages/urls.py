from django.urls import path

from apps.pages.views import DesignSystemPageView, HomePageView, AboutPageView


app_name = "pages"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("design-system/", DesignSystemPageView.as_view(), name="design_system"),
]
