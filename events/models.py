from slugify import slugify
from django.db import models
from home.models import TimestampedModel
from locations.models import Location
from .managers import EventManager, RecurringEventManager, RepeatInfoManager, WeekdayManager
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
    info = models.ForeignKey('RepeatInfo', on_delete=models.CASCADE, default=None)
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

class RepeatInfo(TimestampedModel):
    FREQUENCY_UNITS_CHOICES = [
        (0, 'No Repeat'),
        (1, 'Day(s)'),
        (2, 'Week(s)'),
        (3, 'Month(s)'),
        (4, 'Year(s)'),
    ]
    ENDS_CHOICES = [
        (0, 'Ends after maximum duration (1 year)'),
        (1, 'Ends on date'),
        (2, 'Ends after number of occurences'),
    ]

    weekly = models.BooleanField(default=True)
    frequency = models.PositiveSmallIntegerField(default=1)
    frequency_units = models.PositiveSmallIntegerField(default=0, choices=FREQUENCY_UNITS_CHOICES)
    ends = models.PositiveSmallIntegerField(default=0, choices=ENDS_CHOICES)
    ends_on = models.DateTimeField(null=True, blank=True, default=None)
    ends_after = models.PositiveSmallIntegerField(default=0)
    objects = RepeatInfoManager()

class Weekday(TimestampedModel):
    WEEKDAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    info = models.ForeignKey(RepeatInfo, null=True, blank=True, default=None, on_delete=models.SET_NULL)
    weekday = models.PositiveSmallIntegerField(choices=WEEKDAY_CHOICES)
    objects = WeekdayManager()
