from celery import shared_task
from apps.core.models import Media
import logging

logger = logging.getLogger(__name__)


@shared_task
def media_uploaded(pk):
    media = Media.objects.get(pk=pk)
    logging.info("New media has been uploaded: {}".format(media.file.url))
