import os
import random
import string
from io import BytesIO
from typing import Any, BinaryIO, Dict, List, Tuple

from django.contrib.sites.models import Site
from django.core.files import File
from django.core.mail.message import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http.response import HttpResponse
from django.shortcuts import resolve_url
from django.template.loader import render_to_string
from django.utils.text import slugify
from PIL import Image
from premailer import transform


def unique_slugify(instance, title: str) -> str:
    """
    Returns a unique slug if origin slug is exist.

    The model must have a `slug` field.

    eg: `foo-bar` => `foo-bar-345073`

    Args:
        instance: The model instance to generate unique slug
        title: The value which will be slugified uniquely.
    """
    slug = slugify(title)

    qs = instance.__class__.objects.filter(slug=slug)
    if instance.pk is not None:
        qs = qs.exclude(pk=instance.pk)

    if qs.exists():
        postfix = "".join(random.choices(string.ascii_letters + string.digits, k=6))
        return unique_slugify(instance, f"{slug}-{postfix}")

    return slug


def compress_image(image: BinaryIO, size: Tuple[int, int] = (512, 512)) -> File:
    """
    Compress image using Pillow.

    Transform image to JPEG format with default maximum size of 350x350, but
    still preserving the aspect ratio.
    https://stackoverflow.com/a/33989023/11752450
    """
    im = Image.open(image)
    im_format = im.format
    im.thumbnail(size)
    if im.mode in ("P", "RGBA"):
        im = im.quantize()
    im_io = BytesIO()
    im.save(im_io, im_format, optimize=True, quality=75)
    return File(im_io, image.name)


def send_html_email(
    subject: str,
    to: List[str],
    template_name: str,
    context: Dict[str, Any],
) -> int:
    """
    Sends an HTML and plain text email from a Django template.

    Args:
        subject: The subject of the email.
        to: The list of recipients.
        template_name: The name of the template to render, assumes the plain text
            version is a template with the same name with `.txt` extension.
        context: The context to render the template with.
    """
    context["current_site"] = Site.objects.get_current()

    # html
    html_content = transform(render_to_string(template_name, context))

    # plain text
    text_content_path = os.path.splitext(template_name)[0] + ".txt"
    text_content = render_to_string(text_content_path, context).strip()

    msg = EmailMultiAlternatives(subject, text_content, to=to)
    msg.attach_alternative(html_content, "text/html")
    return msg.send()


def paged_object_list_context(
    queryset: QuerySet,
    page: int,
    per_page: int,
) -> Dict[str, Any]:
    """
    Returns a dictionary with pagination context for template rendering.

    Args:
        queryset: The list of objects to paginate.
        page: The current page number.
        per_page: The number of objects per page.
    """
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page)
    context = {
        "paginator": paginator,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
    }
    return context


def client_redirect(to: str, *args, **kwargs) -> HttpResponse:
    """
    Returns an HttpResponse that triggers HTMX client-side redirect to the
    appropriate URL for the arguments passed.

    The arguments could be:

        * A model: the model's `get_absolute_url()` function will be called.

        * A view name, possibly with arguments: `urls.reverse()` will be used
          to reverse-resolve the name.

        * A URL, which will be used as-is for the redirect location.
    """
    url = resolve_url(to, *args, **kwargs)
    return HttpResponse(status=200, headers={"HX-Redirect": url})
