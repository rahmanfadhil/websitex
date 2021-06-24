from typing import Iterable, Optional

from django.conf import settings


class PaginationMixin:
    """ListView pagination on steroids."""

    paginate_by = [10, 20, 50, 100, 200, 500]

    def get_paginate_by(self, queryset):
        return self.request.GET.get("paginate_by", self.paginate_by[0])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["paginate_by_choices"] = self.paginate_by
        return context


class PageTitleMixin:
    """Customize the page title."""

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
