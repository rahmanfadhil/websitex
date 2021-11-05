from typing import Iterable, List, Optional

from django.db import models
from django.utils import timezone

from apps.core.utils import unique_slugify


class Authorable(models.Model):
    """
    Model can be owned by a registered user.
    """

    author = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)

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

    def publish(self, datetime=None):
        """
        Publish record at a certain time (now if the datetime is not defined).
        """
        if not datetime:
            datetime = timezone.now()
        elif timezone.is_naive(datetime):
            datetime = timezone.make_aware(datetime)
        self.published_at = datetime
        self.save()

    @property
    def is_published(self) -> bool:
        """
        Determine if the record has been published.
        """
        return (
            self.published_at <= timezone.now()
            if self.published_at is not None
            else False
        )

    @property
    def is_draft(self) -> bool:
        """
        Determine if the record is still a draft.
        """
        return not self.is_published

    class Meta:
        abstract = True


class PermalinkableManager(models.Manager):
    """
    Enable automatic slug field generation using bulk_create method.
    """

    def bulk_create(
        self,
        objs: Iterable,
        batch_size: Optional[int],
        ignore_conflicts: bool,
    ) -> List:
        for obj in objs:
            if not obj.slug:
                obj.slug = unique_slugify(obj, obj.get_slug_source())
        return super().bulk_create(
            objs,
            batch_size=batch_size,
            ignore_conflicts=ignore_conflicts,
        )


class Permalinkable(models.Model):
    """
    Generate an SEO friendly slug field.
    """

    slug = models.SlugField(unique=True)

    def get_slug_source(self) -> str:
        raise NotImplemented

    def save(self, *args, **kwargs) -> str:
        if not self.slug:
            self.slug = unique_slugify(self, self.get_slug_source())
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Media(Authorable, Timestampable):
    """
    Store user-uploaded images from /upload-image/ API endpoint, used by the
    rich text editor.
    """

    file = models.ImageField(upload_to="uploads/")

    def __str__(self) -> str:
        return self.file.name
