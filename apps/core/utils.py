from io import BytesIO
from typing import Any, BinaryIO, Dict, List, Tuple, Union

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.files import File
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.db.models import QuerySet
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.text import slugify
from PIL import Image
from premailer import transform


def unique_slugify(klass: type, title: str, instance=None):
    """
    Returns a unique slug if origin slug is exist.

    eg: `foo-bar` => `foo-bar-1`

    Args:
        klass: The model class to perform query.
        title: The value which will be slugified uniquely.
        instance: Exclude a specific model instance if any.
    """
    origin_slug = slugify(title)
    unique_slug = origin_slug
    numb = 1

    if instance is not None:
        while klass.objects.filter(slug=unique_slug).exclude(pk=instance.pk).exists():
            unique_slug = "%s-%d" % (origin_slug, numb)
            numb += 1
    else:
        while klass.objects.filter(slug=unique_slug).exists():
            unique_slug = "%s-%d" % (origin_slug, numb)
            numb += 1

    return unique_slug


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
    email: Union[str, List[str]],
    template_name: str,
    context: Dict[str, Any],
) -> int:
    """
    Renders an HTML template and sends it as email.
    """
    context["current_site"] = Site.objects.get_current()
    html_message = transform(render_to_string(template_name, context))
    message = strip_tags(html_message)
    return send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email] if isinstance(email, str) else email,
        html_message=html_message,
    )


def paged_object_list_context(
    queryset: QuerySet,
    page: int,
    per_page: int,
    max_per_page: int,
) -> Dict[str, Any]:
    """
    Returns a dictionary with pagination context for template rendering.

    Args:
        queryset: The list of objects to paginate.
        page: The current page number.
        per_page: The number of objects per page.
        max_per_page: The maximum number of objects per page.
    """
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page)
    context = {
        "paginator": paginator,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "max_per_page": max_per_page,
    }
    return context
