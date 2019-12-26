import pytz

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
    def create_location(self, name, address1, city, state):
        return self.create(name=name, address1=address1, city=city, state=state)

    def locations_autocomplete(self, request):
        from .models import Location

        query = request.GET.get('q', '')
        locations = []

        if query == '':
            return {'locations': locations}

        for location in Location.objects.filter(name__contains=query) \
        .order_by('name')[:5]:
            locations.append({
                'id': location.id,
                'name': location.name,
            })

        return {'locations': locations}


class EventManager(models.Manager):
    def create_event(self, request):
        from .models import Location, Event, RecurringEvent

        # Data collection
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        all_day_value = request.POST.get('all-day', '')
        date_start_str = request.POST.get('date-start', '')
        date_end_str = request.POST.get('date-end', '')
        frequency = request.POST.get('frequency', -1)
        frequency_units = request.POST.get('frequency-units')
        weekday_list = request.POST.getlist('weekday-list')
        ends = request.POST.get('ends', '-1')
        ends_on_str = request.POST.get('ends-on', '')
        ends_after = request.POST.get('ends-after', '0')
        location_id = request.POST.get('location-id', '0')
        location_name = request.POST.get('location-name', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip-code', '')

        # Data restructuring
        all_day = all_day_value == 'true'

        if frequency:
            frequency = int(frequency)

        if frequency_units:
            frequency_units = int(frequency_units)

        if ends:
            ends = int(ends)

        if ends_after:
            ends_after = int(ends_after)

        if location_id:
            location_id = int(location_id)

        # Basic validations
        errors = []

        if not name:
            errors.append('Please enter a name.')

        if not date_start_str:
            errors.append('Please enter a start date.')

        if not frequency:
            errors.append('Please enter a value for frequency.')

        if frequency_units == '':
            errors.append('Please enter a unit for frequency.')
        elif frequency_units != 0:
            if frequency == -1 or frequency == '':
                errors.append('Please enter a number of repetitions.')

            if ends == 1 and not ends_on_str:
                errors.append('Please enter a date to end on.')

            if ends == 2 and ends_after == 0:
                errors.append('Please enter a number of occurences.')

        if ends == '':
            errors.append('Please enter an end condition.')

        if location_id == 0 and location_name:
            if not address1:
                errors.append('Please enter an address.')

            if not city:
                errors.append('Please enter a city.')

            if not state:
                errors.append('Please enter a state code.')

        if errors:
            return (False, errors)

        # Datetime parsing
        def add_leading_zero_hour(date_str):
            if len(date_str) == 18:
                return date_str[:11] + '0' + date_str[-7:]
            else:
                return date_str

        add_leading_zero_hour(date_start_str)
        date_start = TZ.localize(datetime.strptime(date_start_str, '%m/%d/%Y %I:%M %p'))

        if date_end_str:
            add_leading_zero_hour(date_end_str)
            date_end = TZ.localize(datetime.strptime(date_end_str, '%m/%d/%Y %I:%M %p'))

        if all_day:
            date_start = date_start.replace(hour=0, minute=0, second=0, microsecond=0)

        if ends == 1:
            add_leading_zero_hour(ends_on_str)
            ends_on = TZ.localize(datetime.strptime(ends_on_str, '%m/%d/%Y %I:%M %p'))

        # Grab location object, create new one, or set to None
        if location_id <= 0 and location_name == '':
            location = None
        elif location_id > 0:
            location = Location.objects.get(id=location_id)
        else:
            location = Location.objects.create_location(
                name=location_name,
                address1=address1,
                city=city,
                state=state,
            )

            if address2:
                location.address2 = address2

            if zip_code:
                location.zip_code = zip_code

            location.save()

        kwargs = {}
        if all_day:
            kwargs['all_day'] = all_day

        if date_end_str:
            kwargs['date_end'] = date_end

        if location:
            kwargs['location'] = location

        if frequency_units == 0:
            event = Event.objects.create_single_event(
                name=name,
                date_start=date_start,
                **kwargs
            )
        else:
            if weekday_list:
                kwargs['weekday_list'] = weekday_list

            if date_end_str:
                kwargs['date_end'] = date_end

            if ends == 1:
                kwargs['ends_on'] = ends_on.replace(hour=23, minute=59, second=59, microsecond=999999)
            elif ends == 2:
                kwargs['ends_after'] = ends_after

            events = RecurringEvent.objects.create_recurring_event(
                name=name,
                date_start=date_start,
                frequency=frequency,
                frequency_units=frequency_units,
                ends=ends,
                **kwargs
            )

            events_len = len(events)
            return (True, 'You have successfully added %d event%s.' %
                (events_len, '' if events_len == 1 else 's'))

        return (True, 'You have successfully added 1 event.')

    def create_single_event(self, name, date_start, all_day=False, **kwargs):
        event = self.create(name=name, date_start=date_start.astimezone(pytz.utc), all_day=all_day)

        if not all_day and 'date_end' in kwargs:
            event.date_end = kwargs['date_end'].astimezone(pytz.utc)

        if 'location' in kwargs:
            event.location = kwargs['location']

        event.save()

        return event

    def calendar(self, request):
        from .models import Event

        today = datetime.now(TZ).replace(hour=0, minute=0, second=0, microsecond=0)
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))

        date = first_of_month = datetime(year, month, 1, tzinfo=TZ)
        calendar = []
        while date.weekday() != 6:
            date = date - timedelta(days=1)

        for i in range(42):
            events = Event.objects.filter(
                date_start__date=date,
                date_start__gte=today,
            ).order_by('date_start')[:3]

            events_tz_adjusted = []
            for event in events:
                event.date_start = event.date_start.astimezone(TZ)

                if event.date_end:
                    event.date_end = event.date_end.astimezone(TZ)

                events_tz_adjusted.append(event)

            calendar.append({
                'date': date,
                'events': events_tz_adjusted,
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
        from .models import Event

        today = datetime.now(TZ).replace(hour=0, minute=0, second=0, microsecond=0)
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))

        date = first_of_month = datetime(year, month, 1, tzinfo=TZ)
        calendar = []

        while date.month == first_of_month.month:
            events = Event.objects.filter(
                date_start__date=date,
                date_start__gte=today,
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
        from .models import Event, Location

        today = datetime.now(TZ).replace(hour=0, minute=0, second=0, microsecond=0)
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
                    ).filter(
                        date_start__gte=today,
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
        this_month = datetime.now(TZ).replace(
            day=1, hour=0, minute=0, second=0, microsecond=0)

        month = datetime(
            int(request.GET.get('year', this_month.year)),
            int(request.GET.get('month', this_month.month)),
            1, 0, 0, 0, 0,
        )
        month = TZ.localize(month)

        prev_month = month + relativedelta(months=-1)

        if month == this_month:
            return {
                'disabled': True,
            }
        else:
            return {
                'disabled': False,
                'date': {
                    'year': prev_month.year,
                    'month': prev_month.month,
                }
            }

    def next(self, request):
        this_month = datetime.now(TZ).replace(
            day=1, hour=0, minute=0, second=0, microsecond=0)

        try:
            month = datetime(
                int(request.GET.get('year', this_month.year)),
                int(request.GET.get('month', this_month.month)),
                1, 0, 0, 0, 0,
            )
            month = TZ.localize(month)
        except TypeError:
            return (False, None)

        next_month = month + relativedelta(months=+1)

        return {
            'date': {
                'year': next_month.year,
                'month': next_month.month,
            }
        }

class RecurringEventManager(models.Manager):
    def create_recurring_event(self, name, date_start, frequency, frequency_units, ends, **kwargs):
        from .models import RecurringEvent

        date = date_start
        max_duration = relativedelta(months=+1)
        date_max = date + max_duration
        frequency_units -= 1

        rd_values = [
            relativedelta(days=+frequency),
            relativedelta(days=+(7 * frequency)),
            relativedelta(months=+frequency),
            relativedelta(years=+frequency),
        ]

        first_occurence = None

        days_of_week = [
            'monday',
            'tuesday',
            'wednesday',
            'thursday',
            'friday',
            'saturday',
            'sunday',
        ]

        if ends == 0: # ends after max. duration
            if 'date_end' in kwargs:
                date_end = kwargs['date_end']

                if 'weekday_list' in kwargs and kwargs['weekday_list']:
                    while date <= date_max:
                        if days_of_week[date.weekday()] in kwargs['weekday_list']:
                            event = self.create(name=name, date_start=date.astimezone(pytz.utc))

                            event.date_end = date_end.astimezone(pytz.utc)

                            if first_occurence == None:
                                first_occurence = event.first_occurence = event
                            else:
                                event.first_occurence = first_occurence

                            if 'location' in kwargs:
                                event.location = kwargs['location']

                            event.save()

                        date = date + relativedelta(days=+1)
                        date_end = date_end + relativedelta(days=+1)
                else:
                    while date <= date_max:
                        event = self.create(name=name, date_start=date.astimezone(pytz.utc))

                        event.date_end = date_end.astimezone(pytz.utc)

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
                if 'weekday_list' in kwargs and kwargs['weekday_list']:
                    while date <= date_max:
                        if days_of_week[date.weekday()] in kwargs['weekday_list']:
                            event = self.create(name=name, date_start=date.astimezone(pytz.utc))

                            if 'all_day' in kwargs:
                                event.all_day = kwargs['all_day']
                            else:
                                event.all_day = False

                            if first_occurence == None:
                                first_occurence = event.first_occurence = event
                            else:
                                event.first_occurence = first_occurence

                            if 'location' in kwargs:
                                event.location = kwargs['location']

                            event.save()

                        date = date + relativedelta(days=+1)
                else:
                    while date <= date_max:
                        event = self.create(name=name, date_start=date.astimezone(pytz.utc))

                        if 'all_day' in kwargs:
                            event.all_day = kwargs['all_day']
                        else:
                            event.all_day = False

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

                if 'weekday_list' in kwargs and kwargs['weekday_list']:
                    while date <= kwargs['ends_on'] and date <= date_max:
                        if days_of_week[date.weekday()] in kwargs['weekday_list']:
                            event = self.create(name=name, date_start=date.astimezone(pytz.utc))

                            event.date_end = date_end.astimezone(pytz.utc)

                            if first_occurence == None:
                                first_occurence = event.first_occurence = event
                            else:
                                event.first_occurence = first_occurence

                            if 'location' in kwargs:
                                event.location = kwargs['location']

                            event.save()

                        date = date + relativedelta(days=+1)
                        date_end = date_end + relativedelta(days=+1)
                else:
                    while date <= kwargs['ends_on'] and date <= date_max:
                        event = self.create(name=name, date_start=date.astimezone(pytz.utc))

                        event.date_end = date_end.astimezone(pytz.utc)

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
                if 'weekday_list' in kwargs and kwargs['weekday_list']:
                    while date <= kwargs['ends_on'] and date <= date_max:
                        if days_of_week[date.weekday()] in kwargs['weekday_list']:
                            event = self.create(name=name, date_start=date.astimezone(pytz.utc))

                            if 'all_day' in kwargs:
                                event.all_day = kwargs['all_day']
                            else:
                                event.all_day = False

                            if first_occurence == None:
                                first_occurence = event.first_occurence = event
                            else:
                                event.first_occurence = first_occurence

                            if 'location' in kwargs:
                                event.location = kwargs['location']

                            event.save()

                        date = date + relativedelta(days=+1)
                else:
                    while date <= kwargs['ends_on'] and date <= date_max:
                        event = self.create(name=name, date_start=date.astimezone(pytz.utc))

                        if 'all_day' in kwargs:
                            event.all_day = kwargs['all_day']
                        else:
                            event.all_day = False

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

                if 'weekday_list' in kwargs and kwargs['weekday_list']:
                    i = 0
                    while i < kwargs['ends_after'] and date <= date_max:
                        if days_of_week[date.weekday()] in kwargs['weekday_list']:
                            event = self.create(name=name, date_start=date.astimezone(pytz.utc))

                            event.date_end = date_end.astimezone(pytz.utc)

                            if first_occurence == None:
                                first_occurence = event.first_occurence = event
                            else:
                                event.first_occurence = first_occurence

                            if 'location' in kwargs:
                                event.location = kwargs['location']

                            event.save()

                            i += 1

                        date = date + relativedelta(days=+1)
                        date_end = date_end + relativedelta(days=+1)
                else:
                    i = 0
                    while i < kwargs['ends_after'] and date <= date_max:
                        event = self.create(name=name, date_start=date.astimezone(pytz.utc))

                        event.date_end = date_end.astimezone(pytz.utc)

                        if first_occurence == None:
                            first_occurence = event.first_occurence = event
                        else:
                            event.first_occurence = first_occurence

                        if 'location' in kwargs:
                            event.location = kwargs['location']

                        event.save()

                        i += 1
                        date = date + rd_values[frequency_units]
                        date_end = date_end + rd_values[frequency_units]
            else:
                if 'weekday_list' in kwargs and kwargs['weekday_list']:
                    i = 0
                    while i < kwargs['ends_after'] and date <= date_max:
                        if days_of_week[date.weekday()] in kwargs['weekday_list']:
                            event = self.create(name=name, date_start=date.astimezone(pytz.utc))

                            if 'all_day' in kwargs:
                                event.all_day = kwargs['all_day']
                            else:
                                event.all_day = False

                            if first_occurence == None:
                                first_occurence = event.first_occurence = event
                            else:
                                event.first_occurence = first_occurence

                            if 'location' in kwargs:
                                event.location = kwargs['location']

                            event.save()

                            i += 1

                        date = date + relativedelta(days=+1)
                else:
                    i = 0
                    while i < kwargs['ends_after'] and date <= date_max:
                        event = self.create(name=name, date_start=date.astimezone(pytz.utc))

                        if 'all_day' in kwargs:
                            event.all_day = kwargs['all_day']
                        else:
                            event.all_day = False

                        if first_occurence == None:
                            first_occurence = event.first_occurence = event
                        else:
                            event.first_occurence = first_occurence

                        if 'location' in kwargs:
                            event.location = kwargs['location']

                        event.save()

                        i += 1
                        date = date + rd_values[frequency_units]

        return RecurringEvent.objects.filter(first_occurence=first_occurence)
