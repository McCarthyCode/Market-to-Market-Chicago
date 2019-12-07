from django.db import models
from home.models import TimestampedModel
from .managers import LocationManager, EventManager, RecurringEventManager

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
    all_day = models.BooleanField(default=False)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField(null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE)
    objects = EventManager()

    def __str__(self):
        if self.location and self.date_end:
            return self.name + ' at ' + self.location.name + ' - ' + self.date_start.strftime('%a. %b. %-d, %Y (%-I:%S %p–') + self.date_end.strftime('%-I:%S %p)')
        elif self.location and not self.date_end:
            return self.name + ' at ' + self.location.name + ' - ' + self.date_start.strftime('%a. %b. %-d, %Y (%-I:%S %p)')
        elif not self.location and self.date_end:
            return self.name + ' - ' + self.date_start.strftime('%a. %b. %-d, %Y (%-I:%S %p–') +self.date_end.strftime('%-I:%S %p)')
        else:
            return self.name + ' - ' + self.date_start.strftime('%a. %b. %-d, %Y (%-I:%S %p)')

class RecurringEvent(Event):
    FREQUENCY_UNITS_CHOICES = (
        (0, 'Days'),
        (1, 'Weeks'),
        (2, 'Months'),
        (3, 'Years'),
    )
    ENDS_CHOICES = (
        (0, 'after max. duration (6 months)'),
        (1, 'on ___'),
        (2, 'after ___ occurences'),
    )
    first_occurence = models.ForeignKey('self', null=True, blank=True, editable=False, default=None, on_delete=models.SET_NULL)
    objects = RecurringEventManager()

    def __str__(self):
        if self.location and self.date_end:
            return self.name + ' at ' + self.location.name + ' - ' + self.date_start.strftime('%a. %b. %-d, %Y (%-I:%S %p–') + self.date_end.strftime('%-I:%S %p)')
        elif self.location and not self.date_end:
            return self.name + ' at ' + self.location.name + ' - ' + self.date_start.strftime('%a. %b. %-d, %Y (%-I:%S %p)')
        elif not self.location and self.date_end:
            return self.name + ' - ' + self.date_start.strftime('%a. %b. %-d, %Y (%-I:%S %p–') +self.date_end.strftime('%-I:%S %p)')
        else:
            return self.name + ' - ' + self.date_start.strftime('%a. %b. %-d, %Y (%-I:%S %p)')
