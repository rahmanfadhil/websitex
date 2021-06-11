from django import forms
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from apps.core.forms import CrispyFormMixin
from apps.core.mixins import PageTitleMixin
from apps.core.models import Media
from apps.pages.tasks import media_uploaded


class MediaForm(forms.ModelForm, CrispyFormMixin):
    class Meta:
        model = Media
        fields = ("file",)


class HomePageView(CreateView):
    template_name = "pages/home.html"
    form_class = MediaForm
    success_url = reverse_lazy("pages:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        media_uploaded.delay(form.instance.pk)
        return response


class AboutPageView(PageTitleMixin, TemplateView):
    page_title = "About"
    template_name = "pages/about.html"
