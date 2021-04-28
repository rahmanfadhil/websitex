from io import BytesIO
from os import path
from typing import Tuple

from django.conf import settings
from django.core.files import File
from django.core.mail import send_mail
from django.db.models.fields.files import ImageFieldFile
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.text import slugify
from PIL import Image


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


def compress_image(image: ImageFieldFile, size: Tuple[int, int] = (512, 512)) -> File:
    """
    Compress image using Pillow.

    Transform image to JPEG format with default maximum size of 350x350, but
    still preserving the aspect ratio.
    https://stackoverflow.com/a/33989023/11752450
    """
    im = Image.open(image)
    format = im.format
    im = im.quantize()
    im.thumbnail(size)
    im_io = BytesIO()
    im.save(im_io, format)
    return File(im_io, name=image.name)


def send_html_email(subject: str, email: str, template_name: str, context: dict) -> int:
    """
    Send email from HTML template.
    """
    html_message = render_to_string(template_name, context)
    message = strip_tags(html_message)
    return send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        html_message=html_message,
        fail_silently=True,
    )
