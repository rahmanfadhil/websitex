from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.http.response import HttpResponse, JsonResponse
from django.views.generic.edit import CreateView

from apps.core.models import Authorable, Media
from apps.core.utils import compress_image


# ABSTRACT VIEWS
# ------------------------------------------------------------------------------


class AuthorableCreateViewMeta(type):
    """
    Make sure that the model used in AuthorableCreateView is a subclass of
    Authorable abstract model.
    """

    def __new__(cls, name, bases, body):
        if name != "AuthorableCreateView" and not issubclass(body["model"], Authorable):
            raise ImproperlyConfigured(
                "Model must be a subclass of Authorable in order to be used in the AuthorableCreateView"
            )
        return super().__new__(cls, name, bases, body)


class AuthorableCreateView(
    LoginRequiredMixin, CreateView, metaclass=AuthorableCreateViewMeta
):
    """
    Set the currently logged-in user as the author of the model.
    """

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# URL VIEWS
# ------------------------------------------------------------------------------


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
