from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.edit import CreateView

from apps.core.models import Authorable


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
    CreateView, LoginRequiredMixin, metaclass=AuthorableCreateViewMeta
):
    """
    Set the currently logged-in user as the author of the model.
    """

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
