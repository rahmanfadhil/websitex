from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    full_name = models.CharField(_("full name"), max_length=150, null=True, blank=True)
    first_name = None
    last_name = None
    avatar = models.ImageField(upload_to="user_avatar/", null=True, blank=True)

    def get_full_name(self) -> str:
        return self.full_name

    def __str__(self):
        return self.email
