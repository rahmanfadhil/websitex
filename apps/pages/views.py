from django.views.generic import FormView, TemplateView

from apps.core.mixins import PageTitleMixin
from apps.pages.forms import DesignSystemForm
from django.urls import reverse_lazy


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(PageTitleMixin, TemplateView):
    page_title = "About"
    template_name = "pages/about.html"


class DesignSystemPageView(PageTitleMixin, FormView):
    page_title = "Design System"
    template_name = "pages/design_system.html"
    form_class = DesignSystemForm
    success_url = reverse_lazy("pages:home")

    def get_template_names(self):
        if self.request.GET.get("modal"):
            return ["snippets/form.html"]
        return super().get_template_names()
