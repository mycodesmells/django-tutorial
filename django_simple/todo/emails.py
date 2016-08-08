import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Task)
def send_mail_on_task_save(sender, instance, **kwargs):
    logger.warning("Sending email as task \"%s\" has been saved." % instance.name)