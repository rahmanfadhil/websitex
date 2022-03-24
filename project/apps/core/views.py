import json
from http import HTTPStatus

from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django.views.decorators.http import require_POST

from apps.core.forms import MediaForm
from apps.core.utils import compress_image


@require_POST
def js_upload_media(request: HttpRequest) -> HttpResponse:
    """
    Upload an image to the server.
    """
    form = MediaForm(request.POST, request.FILES)

    if form.is_valid():
        media = form.save(commit=False)
        media.file = compress_image(media.file, (1024, 1024))
        if request.user.is_authenticated:
            media.user = request.user
        media.save()

        # Return the URL of the image.
        url = request.build_absolute_uri(media.file.url)
        return JsonResponse({"url": url})
    else:
        return JsonResponse(
            {"errors": form.errors.as_data()},
            status=HTTPStatus.BAD_REQUEST,
        )


@require_POST
def js_reverse(request: HttpRequest) -> HttpResponse:
    """
    Returns the absolute url of a view.
    """
    try:
        data = json.loads(request.body)
        url = reverse(data["name"], args=data.get("args"), kwargs=data.get("kwargs"))
        return HttpResponse(url)
    except NoReverseMatch:
        return HttpResponse("No reverse match!", status=400)
