from apps.pages.tasks import hello
from django.views.generic import TemplateView
from django.core.cache import cache

from apps.core.mixins import PageTitleMixin


class HomePageView(TemplateView):
    template_name = "pages/home.html"

    def dispatch(self, request, *args, **kwargs):
        hello.delay()
        cache.set("hello", "world", 5)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hello"] = cache.get("hello")
        return context


class AboutPageView(PageTitleMixin, TemplateView):
    page_title = "About"
    template_name = "pages/about.html"
