from io import BytesIO
from typing import Any, BinaryIO, Dict, List, Tuple, Union

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.files import File
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from django.http.request import HttpRequest
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
    im.save(im_io, im_format)
    return File(im_io, image.name)


def send_html_email(
    request: HttpRequest,
    subject: str,
    email: Union[str, List[str]],
    template_name: str,
    context: Dict[str, Any],
) -> int:
    """
    Renders an HTML template and sends it as email.
    """
    context["current_site"] = get_current_site(request)
    html_message = transform(render_to_string(template_name, context))
    message = strip_tags(html_message)
    return send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email] if isinstance(email, str) else email,
        html_message=html_message,
    )
