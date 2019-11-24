# import pytz

from django.db import models
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from mtm.settings import TZ


class EventManager(models.Manager):
    def calendar_month(self, request):
        from events.models import Event

        today = datetime.now(TZ)
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))

        date = first_of_month = datetime(year, month, 1, tzinfo=TZ)
        calendar = []
        while date.weekday() != 6:
            date = date - timedelta(days=1)

        for i in range(42):
            events = Event.events.filter(
                date_start__date=date,
            )

            print(i)

            calendar.append({
                'date': date,
                'events': events,
                'row': int(i / 7),
                'col': i % 7,
            })

            date = date + timedelta(days=1)

        return {
            'date': first_of_month,
            'calendar': calendar,
            'days_of_week': [
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
            ],
            'prev': first_of_month + relativedelta(months=-1),
            'next': first_of_month + relativedelta(months=+1),
        }