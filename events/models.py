from django.db import models
from home.models import TimestampedModel

class Location(TimestampedModel):
    name = models.CharField(max_length=200)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(null=True, blank=True, max_length=200)
    city = models.CharField(max_length=80, default='Chicago')
    state = models.CharField(max_length=2, default='IL')
    zip = models.CharField(null=True, blank=True, max_length=5)

    def __str__(self):
        return self.name


class Event(TimestampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
