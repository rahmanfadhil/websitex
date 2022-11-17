from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
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
    body = RichTextField(blank=True)
    thumbnail = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    search_fields = Page.search_fields + [
        index.SearchField("date"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("body", classname="full"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel("thumbnail"),
    ]

    class Meta:
        ordering = ["-date"]
