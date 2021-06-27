import json
from http import HTTPStatus

from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView

from apps.core.models import Media
from apps.core.utils import compress_image


class MediaCreateView(CreateView):
    """
    Handle media uploads from Trix editor.
    """

    model = Media
    fields = ("file",)

    def form_invalid(self, form) -> HttpResponse:
        # Returns the form errors in a JSON format.
        return JsonResponse(
            {"errors": form.errors},
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    def form_valid(self, form) -> HttpResponse:
        # Compress the image before saving.
        form.instance.file = compress_image(form.instance.file, (2048, 2048))

        # If the user is logged in, save the user information who uploads the file.
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user

        # Save the image to the database.
        media = form.save()

        # Return the absolute url of the file.
        return JsonResponse({"url": self.request.build_absolute_uri(media.file.url)})


@require_POST
def js_reverse(request: HttpRequest) -> HttpResponse:
    try:
        data = json.loads(request.body)
        url = reverse(data["name"], args=data.get("args"), kwargs=data.get("kwargs"))
        return HttpResponse(url)
    except NoReverseMatch:
        return HttpResponse("No reverse match!", status=400)
