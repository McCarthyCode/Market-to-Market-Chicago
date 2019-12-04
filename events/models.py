from django.db import models
from home.models import TimestampedModel
from .managers import LocationManager, EventManager

class Location(TimestampedModel):
    name = models.CharField(max_length=200)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(null=True, blank=True, max_length=200)
    city = models.CharField(max_length=80, default='Chicago')
    state = models.CharField(max_length=2, default='IL')
    zip_code = models.CharField(null=True, blank=True, max_length=5)
    objects = LocationManager()

    def __str__(self):
        return self.name

class Event(TimestampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField(null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE)
    objects = EventManager()

    def __str__(self):
        return self.name
