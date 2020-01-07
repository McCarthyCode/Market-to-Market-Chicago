from slugify import slugify
from django.db import models
from home.models import TimestampedModel
from locations.models import Location
from .managers import EventManager, RecurringEventManager
from mtm.settings import TZ

class Event(TimestampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(default='', max_length=100, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    all_day = models.BooleanField(default=False)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField(null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE)
    objects = EventManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.location:
            if self.date_end:
                return self.name + ' at ' + self.location.name + ' - ' + self.date_start.astimezone(TZ).strftime('%a. %b. %-d, %Y (%-I:%M %p–') + self.date_end.astimezone(TZ).strftime('%-I:%M %p)')
            elif self.all_day:
                return self.name + ' at ' + self.location.name + ' - ' + self.date_start.astimezone(TZ).strftime('%a. %b. %-d, %Y (All Day)')
            else:
                return self.name + ' at ' + self.location.name + ' - ' + self.date_start.astimezone(TZ).strftime('%a. %b. %-d, %Y (%-I:%M %p)')
        else:
            if self.date_end:
                return self.name + ' - ' + self.date_start.astimezone(TZ).strftime('%a. %b. %-d, %Y (%-I:%M %p–') + self.date_end.astimezone(TZ).strftime('%-I:%M %p)')
            elif self.all_day:
                return self.name + ' - ' + self.date_start.astimezone(TZ).strftime('%a. %b. %-d, %Y (All Day)')
            else:
                return self.name + ' - ' + self.date_start.astimezone(TZ).strftime('%a. %b. %-d, %Y (%-I:%M %p)')

class RecurringEvent(Event):
    first_occurence = models.ForeignKey('self', null=True, blank=True, default=None, on_delete=models.SET_NULL)
    weekly = models.BooleanField(default=True)
    objects = RecurringEventManager()

    def __str__(self):
        if self.location:
            if self.date_end:
                return self.name + ' at ' + self.location.name + ' - ' + self.date_start.astimezone(TZ).strftime('%a. %b. %-d, %Y (%-I:%M %p–') + self.date_end.astimezone(TZ).strftime('%-I:%M %p)')
            elif self.all_day:
                return self.name + ' at ' + self.location.name + ' - ' + self.date_start.astimezone(TZ).strftime('%a. %b. %-d, %Y (All Day)')
            else:
                return self.name + ' at ' + self.location.name + ' - ' + self.date_start.astimezone(TZ).strftime('%a. %b. %-d, %Y (%-I:%M %p)')
        else:
            if self.date_end:
                return self.name + ' - ' + self.date_start.astimezone(TZ).strftime('%a. %b. %-d, %Y (%-I:%M %p–') + self.date_end.astimezone(TZ).strftime('%-I:%M %p)')
            elif self.all_day:
                return self.name + ' - ' + self.date_start.astimezone(TZ).strftime('%a. %b. %-d, %Y (All Day)')
            else:
                return self.name + ' - ' + self.date_start.astimezone(TZ).strftime('%a. %b. %-d, %Y (%-I:%M %p)')
