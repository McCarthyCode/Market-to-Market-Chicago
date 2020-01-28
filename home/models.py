from django.db import models

from mtm.settings import TZ

class TimestampedModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def updated_later(self):
        return self.date_updated.astimezone(TZ).replace(hour=0, minute=0, second=0, microsecond=0) > self.date_created.astimezone(TZ).replace(hour=0, minute=0, second=0, microsecond=0)

    class Meta:
        abstract = True
