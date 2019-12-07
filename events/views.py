from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from mtm.settings import TZ, NAME
from .models import Location, Event, RecurringEvent

def index(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    # RecurringEvent.objects.create_recurring_event(
    #     'Karaoke',
    #     datetime(2019, 12, 8, 20, 0, 0),
    #     1,
    #     1,
    #     1,
    #     date_end=datetime(2019, 12, 9, 0, 0, 0),
    #     ends_on=datetime(2020, 1, 26, 20, 0, 0),
    #     location=Location.objects.get(name='Bobby Love\'s'),
    # )

    return render(request, 'events/index.html', {
        'calendar': Event.objects.calendar(request),
        'by_date': Event.objects.by_date(request),
        'by_location': Event.objects.by_location(request),
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def month(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'events/month.html', Event.objects.calendar(request))

def prev(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'events/month.html', Event.objects.prev(request))

def next(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'events/month.html', Event.objects.next(request))
