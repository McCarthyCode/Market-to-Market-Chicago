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
    def create_event(self, request):
        return (True, 'You have successfully added an event.')

    def create_single_event(self, name, date_start):
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

        while date.month == first_of_month.month:
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

    def by_location(self, request):
        from events.models import Event, Location

        today = datetime.now(TZ)
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))

        date = first_of_month = datetime(year, month, 1, tzinfo=TZ)
        locations = []

        for location in Location.objects.all().order_by('name')[:30]:
            if Event.objects.filter(
                location=location,
                date_start__gte=first_of_month,
                date_start__lt=first_of_month + relativedelta(months=+1),
            ):
                day = first_of_month
                event_tree = []
                while day < first_of_month + relativedelta(months=+1):
                    events_on_day = Event.objects.filter(
                        location=location,
                        date_start__gte=day,
                        date_start__lt=day + relativedelta(days=+1),
                    ).order_by('date_start')

                    if len(events_on_day) > 0:
                        event_tree.append({
                            'date': day,
                            'events': events_on_day,
                        })

                    day = day + relativedelta(days=+1)

                locations.append({
                    'location': location,
                    'event_tree': event_tree,
                })

        return {
            'date': first_of_month,
            'locations': locations,
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

class RecurringEventManager(models.Manager):
    def create_recurring_event(self, name, date_start, frequency, frequency_units, ends, **kwargs):
        from .models import RecurringEvent

        date = date_start
        max_duration = relativedelta(months=+6)
        date_max = date + max_duration

        rd_values = [
            relativedelta(days=+frequency),
            relativedelta(days=+(7 * frequency)),
            relativedelta(months=+frequency),
            relativedelta(years=+frequency),
        ]

        first_occurence = None

        if ends == 0: # ends after max. duration
            if 'date_end' in kwargs:
                date_end = kwargs['date_end']

                while date <= date_max:
                    event = self.create(name=name, date_start=date, date_end=date_end)

                    if first_occurence == None:
                        first_occurence = event.first_occurence = event
                    else:
                        event.first_occurence = first_occurence

                    if 'location' in kwargs:
                        event.location = kwargs['location']

                    event.save()

                    date = date + rd_values[frequency_units]
                    date_end = date_end + rd_values[frequency_units]
            else:
                while date <= date_max:
                    event = self.create(name=name, date_start=date)

                    if first_occurence == None:
                        first_occurence = event.first_occurence = event
                    else:
                        event.first_occurence = first_occurence

                    if 'location' in kwargs:
                        event.location = kwargs['location']

                    event.save()

                    date = date + rd_values[frequency_units]
        elif ends == 1: # ends on date
            if 'ends_on' not in kwargs:
                raise TypeError("create_recurring_event() missing 1 required keyword argument 'ends_on'")

            if 'date_end' in kwargs:
                date_end = kwargs['date_end']

                while date <= kwargs['ends_on'] and date <= date_max:
                    event = self.create(name=name, date_start=date, date_end=date_end)

                    if first_occurence == None:
                        first_occurence = event.first_occurence = event
                    else:
                        event.first_occurence = first_occurence

                    if 'location' in kwargs:
                        event.location = kwargs['location']

                    event.save()

                    date = date + rd_values[frequency_units]
                    date_end = date_end + rd_values[frequency_units]
            else:
                while date <= kwargs['ends_on'] and date <= date_max:
                    event = self.create(name=name, date_start=date)

                    if first_occurence == None:
                        first_occurence = event.first_occurence = event
                    else:
                        event.first_occurence = first_occurence

                    if 'location' in kwargs:
                        event.location = kwargs['location']

                    event.save()

                    date = date + rd_values[frequency_units]
        elif ends == 2: # ends after a number of occurences
            if 'ends_after' not in kwargs:
                raise TypeError("create_recurring_event() missing 1 required keyword argument 'ends_after'")

            if 'date_end' in kwargs:
                date_end = kwargs['date_end']

                for _ in range(kwargs['ends_after']):
                    if date > date_max:
                        break

                    event = self.create(name=name, date_start=date, date_end=date_end)

                    if first_occurence == None:
                        first_occurence = event.first_occurence = event
                    else:
                        event.first_occurence = first_occurence

                    if 'location' in kwargs:
                        event.location = kwargs['location']

                    event.save()

                    date = date + rd_values[frequency_units]
                    date_end = date_end + rd_values[frequency_units]
            else:
                for _ in range(kwargs['ends_after']):
                    if date > date_max:
                        break

                    event = self.create(name=name, date_start=date)

                    if first_occurence == None:
                        first_occurence = event.first_occurence = event
                    else:
                        event.first_occurence = first_occurence

                    if 'location' in kwargs:
                        event.location = kwargs['location']

                    event.save()

                    date = date + rd_values[frequency_units]

        return RecurringEvent.objects.filter(first_occurence=first_occurence)
