import os
from io import BytesIO
from typing import Optional, Tuple

from django.core.files import File
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

    queryset = klass.objects.filter(slug=unique_slug)

    if instance is not None:
        queryset = queryset.exclude(pk=instance.pk)

    while queryset.exists():
        unique_slug = "%s-%d" % (origin_slug, numb)
        numb += 1

    return unique_slug


def duplicate_image(image) -> Optional[File]:
    """
    Returns a duplicate image from other model field or None if the image is
    not provided or something went wrong.
    """
    try:
        im_io = BytesIO()
        Image.open(image).save(im_io, "JPEG", quality=70)
        return File(im_io, name=os.path.basename(image))
    except:
        return None


def compress_image(image, size: Tuple[int, int] = (350, 350)) -> File:
    """
    Compress image using Pillow.

    Transform image to JPEG format with default maximum size of 350x350, but
    still preserving the aspect ratio.
    https://stackoverflow.com/a/33989023/11752450
    """
    im = Image.open(image)
    im.thumbnail(size)
    im_io = BytesIO()
    im.save(im_io, "JPEG", quality=70)
    return File(im_io, name=image.name)
