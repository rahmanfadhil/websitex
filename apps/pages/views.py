from django.views.generic import TemplateView

from apps.core.mixins import PageTitleMixin


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(PageTitleMixin, TemplateView):
    page_title = "About"
    template_name = "pages/about.html"
