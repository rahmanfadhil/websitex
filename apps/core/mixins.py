from typing import Iterable, Optional

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.utils import timezone
from django.contrib.messages import views as messages_views


class PaginationMixin:
    """
    ListView pagination on steroids.
    """

    paginate_by = [10, 20, 50, 100, 200, 500]

    def get_paginate_by(self, queryset):
        return self.request.GET.get("paginate_by", self.paginate_by[0])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["paginate_by_choices"] = self.paginate_by
        return context


class PageTitleMixin:
    """
    Customize the page title.
    """

    page_title: Optional[str] = None

    def get_page_title(self) -> str:
        if self.page_title is None:
            raise NotImplementedError(
                "Please implement either the `page_title` property, `get_page_title` method, or `get_full_page_title` method."
            )
        return self.page_title

    def get_full_page_title(self) -> str:
        return "{} - {}".format(self.get_page_title(), settings.PAGE_TITLE)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.get_full_page_title()
        return context


class MetaTagsMixin:
    """
    Customize page meta tags for SEO.
    """

    def get_meta_description(self) -> str:
        return settings.DEFAULT_META_DESCRIPTION

    def get_meta_keywords(self) -> Iterable[str]:
        return settings.DEFAULT_META_KEYWORDS

    def get_meta_author(self) -> str:
        return settings.DEFAULT_META_AUTHOR

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta_description"] = self.get_meta_description()
        context["meta_keywords"] = ", ".join(self.get_meta_keywords())
        context["meta_author"] = self.get_meta_author()
        return context


class OnlyPublishedMixin:
    """
    Mixin that filters the queryset to only return published objects.
    """

    def get_queryset(self):
        return super().get_queryset().filter(published_at__gte=timezone.now())


class AuthorableMixin(LoginRequiredMixin):
    """
    Mixin for a generic view that uses Authorable model.
    """

    def get_queryset(self):
        # Make sure it only return objects created by the current user.
        return super().get_queryset().filter(author=self.request.user)

    def form_valid(self, form) -> HttpResponse:
        # Assign the current user as the author of the model.
        if form.instance.author is None:
            form.instance.author = self.request.user
        return super().form_valid(form)


class SuccessMessageMixin:
    """
    Add a success message on successful form submission and object deletion.
    """

    success_message = ""

    def delete(self, *args, **kwargs):
        response = super().delete(*args, **kwargs)
        self._show_message()
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        self._show_message()
        return response

    def _show_message(self):
        success_message = self.get_success_message(self.object.__dict__)
        if success_message:
            messages.success(self.request, success_message)

    def get_success_message(self, data):
        return self.success_message % data
