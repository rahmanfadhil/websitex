from django.db import models


class Authorable(models.Model):
    """
    Model can be owned by a registered user.
    """

    author = models.ForeignKey("users.User", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Timestampable(models.Model):
    """
    Maintain the created_at and updated_at columns.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Publishable(models.Model):
    """
    Implement draft and publish feature.
    """

    is_published = models.BooleanField(default=False)

    class Meta:
        abstract = True
