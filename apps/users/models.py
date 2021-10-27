from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.utils import send_html_email


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator(
        regex=r"^[\w-]+\Z",
        message=_(
            "Enter a valid username. This value may contain only letters, "
            "numbers, underscores, and hyphens."
        ),
    )

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits, underscores, and hyphens only."
        ),
        validators=[username_validator],
        error_messages={"unique": _("A user with that username already exists.")},
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

    def send_login_link(self, next_url: str):
        send_html_email(
            subject="Login",
            email=self.email,
            template_name="emails/login.html",
            context={"url": next_url, "user": self},
        )

    def __str__(self):
        return self.email
