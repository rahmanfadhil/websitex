from django.views.generic.edit import FormView
from apps.core.widgets import MoneyInput, TrixEditorInput
from django import forms
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from apps.core.forms import CrispyFormMixin
from apps.core.mixins import PageTitleMixin
from apps.core.models import Media


class MediaForm(forms.Form, CrispyFormMixin):
    description = forms.CharField(widget=TrixEditorInput)


class HomePageView(FormView):
    template_name = "pages/home.html"
    form_class = MediaForm
    success_url = reverse_lazy("pages:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class AboutPageView(PageTitleMixin, TemplateView):
    page_title = "About"
    template_name = "pages/about.html"
