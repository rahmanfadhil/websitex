from django.db import models
from django.db.models.query_utils import Q
from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import naturaltime

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

    @property
    def created_since(self) -> str:
        return naturaltime(self.created_at)

    @property
    def updated_since(self) -> str:
        return naturaltime(self.created_at)

    class Meta:
        abstract = True


class PublishableQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published_at__lte=timezone.now())

    def draft(self):
        return self.filter(
            Q(published_at__isnull=True) | Q(published_at__gt=timezone.now())
        )


class Publishable(models.Model):
    """
    Implement draft and publish feature.
    """

    published_at = models.DateTimeField(null=True, blank=True)

    @property
    def published_since(self) -> str:
        return naturaltime(self.published_at)

    def publish_on(self, datetime=None):
        """
        Publish record at a certain time.
        """
        if not datetime:
            datetime = timezone.now()
        elif timezone.is_naive(datetime):
            datetime = timezone.make_aware(datetime)
        self.publish_date = datetime
        self.save()

    @property
    def is_published(self):
        """
        Determine if the record is published or not.
        """
        return self.publish_date < timezone.now()

    class Meta:
        abstract = True


class Permalinkable(models.Model):
    """
    Generate an SEO friendly slug field.
    """

    slug = models.SlugField(unique=True)

    def get_slug_source(self) -> str:
        raise NotImplemented

    def save(self, *args, **kwargs) -> str:
        if not self.slug:
            self.slug = unique_slugify(self.__class__, self.get_slug_source())
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True
