import logging

from django.db import models

logger = logging.getLogger(__name__)


class Task(models.Model):
    name = models.TextField(max_length=100)
    done = models.BooleanField(default=False)

    def __str__(self):
        if self.done:
            return "[✔] %s" % self.name
        else:
            return "[✖] %s" % self.name

    def save(self, *args, **kwargs):
        logger.warning("Task model change (name=%s)" % self.name)
        super(Task, self).save(*args, **kwargs)