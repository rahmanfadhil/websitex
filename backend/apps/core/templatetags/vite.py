import json
import os

from django.conf import settings
from django.contrib.staticfiles import finders
from django.template import Library
from django.utils.safestring import mark_safe

register = Library()

DIST_URL = os.path.join(settings.STATIC_URL, "dist")


def get_html_tags(*files: str) -> str:
    html = ""
    for file in files:
        if file.endswith(".css"):
            html += f'<link rel="stylesheet" href="{file}">'
        else:
            html += f'<script type="module" src="{file}"></script>'
    return mark_safe(html)


@register.simple_tag
def load_vite(name: str) -> str:
    """Load a Vite asset from the manifest."""
    if settings.DEBUG:
        return get_html_tags(
            "http://localhost:5173/static/dist/@vite/client",
            f"http://localhost:5173/static/dist/{name}",
        )
    else:
        with open(finders.find("dist/manifest.json")) as manifest:
            data = json.load(manifest)[name]
            tags = [os.path.join(DIST_URL, data["file"])]
            for file in data.get("css", []):
                tags.append(os.path.join(DIST_URL, file))
            return get_html_tags(*tags)
