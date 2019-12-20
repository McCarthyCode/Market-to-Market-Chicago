from django.db import models
from home.models import TimestampedModel
from .managers import LocationManager, EventManager, RecurringEventManager
from mtm.settings import TZ

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
    description = models.TextField(max_length=1000, null=True, blank=True)
    all_day = models.BooleanField(default=False)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField(null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE)
    objects = EventManager()

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
