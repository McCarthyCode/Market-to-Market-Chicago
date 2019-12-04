# import pytz

from django.db import models
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from mtm.settings import TZ


DOW = [
    {
        'col': 0,
        'dow': 'Sun',
    },
    {
        'col': 1,
        'dow': 'Mon',
    },
    {
        'col': 2,
        'dow': 'Tue',
    },
    {
        'col': 3,
        'dow': 'Wed',
    },
    {
        'col': 4,
        'dow': 'Thu',
    },
    {
        'col': 5,
        'dow': 'Fri',
    },
    {
        'col': 6,
        'dow': 'Sat',
    },
]


class LocationManager(models.Manager):
    def create_location(self, name, address1):
        return self.create(name=name, address1=address1)


class EventManager(models.Manager):
    def create_event(self, name, date_start):
        return self.create(name=name, date_start=date_start)

    def calendar(self, request):
        from events.models import Event

        today = datetime.now(TZ)
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))

        date = first_of_month = datetime(year, month, 1, tzinfo=TZ)
        calendar = []
        while date.weekday() != 6:
            date = date - timedelta(days=1)

        for i in range(42):
            events = Event.objects.filter(
                date_start__date=date,
            ).order_by('date_start')

            calendar.append({
                'date': date,
                'events': events if len(events) < 4 else events[:3],
                'row': int(i / 7),
                'col': i % 7,
            })

            date = date + timedelta(days=1)

        return {
            'date': first_of_month,
            'calendar': calendar,
            'days_of_week': DOW,
        }

    def by_date(self, request):
        from events.models import Event

        today = datetime.now(TZ)
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))

        date = first_of_month = datetime(year, month, 1, tzinfo=TZ)
        calendar = []
        while date.weekday() != 6:
            date = date - timedelta(days=1)

        for i in range(42):
            events = Event.objects.filter(
                date_start__date=date,
            ).order_by('date_start')

            calendar.append({
                'date': date,
                'events': events,
            })

            date = date + timedelta(days=1)

        return {
            'date': first_of_month,
            'calendar': calendar,
        }

    def prev(self, request):
        this_month = datetime.now(tz).replace(
            hour=0, minute=0, second=0, microsecond=0)

        try:
            month = datetime(
                int(request.GET.get('year', today.year)),
                int(request.GET.get('month', today.month)),
                1, 0, 0, 0, 0,
            )
            month = tz.localize(month)
        except TypeError:
            return (False, None)

        prev_month = month + relativedelta(months=-1)

        if month == this_month:
            return (True, {
                'disabled': True,
            })
        else:
            return (True, {
                'disabled': False,
                'date': {
                    'year': prev_month.year,
                    'month': prev_month.month,
                }
            })

    def next(self, request):
        try:
            month = datetime(
                int(request.GET.get('year', today.year)),
                int(request.GET.get('month', today.month)),
                1, 0, 0, 0, 0,
            )
            month = tz.localize(month)
        except TypeError:
            return (False, None)

        next_month = month + relativedelta(months=+1)

        return (True, {
            'date': {
                'year': next_month.year,
                'month': next_month.month,
            }
        })
