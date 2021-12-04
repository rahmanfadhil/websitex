from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.search import index


class BlogIndexPage(Page):
    intro = models.CharField(max_length=250)

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]

    def get_children(self):
        return super().get_children().live().order_by("-blogpage__date")


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("body", classname="full"),
    ]

    class Meta:
        ordering = ["-date"]
