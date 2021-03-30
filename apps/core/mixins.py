from typing import Iterable, Optional

from django.conf import settings


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
        return "{} - {}".format(self.get_page_title(), settings.PROJECT_NAME)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.get_full_page_title()
        return context


class MetaTagsMixin:
    def get_meta_description(self) -> str:
        raise NotImplemented

    def get_meta_keywords(self) -> Iterable[str]:
        raise NotImplemented

    def get_meta_author(self) -> str:
        raise NotImplemented

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta_description"] = self.get_meta_description()
        context["meta_keywords"] = ", ".join(self.get_meta_keywords())
        context["meta_author"] = self.get_meta_author()
        return context
