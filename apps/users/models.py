from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "150 characters or fewer. Letters, numbers, underscores, and hyphens only."
        ),
        validators=[validators.validate_slug],
        error_messages={
            "unique": _("A user with that username already exists."),
            "invalid": _(
                "Enter a valid username consisting of letters, numbers, underscores or hyphens."
            ),
        },
        null=True,
    )
    email = models.EmailField(_("email address"), unique=True)
    full_name = models.CharField(_("full name"), max_length=150, null=True, blank=True)
    first_name = None
    last_name = None
    avatar = models.ImageField(
        _("profile picture"),
        upload_to="user_avatar/",
        null=True,
        blank=True,
    )

    def get_full_name(self) -> str:
        return self.full_name

    def __str__(self):
        return self.email
