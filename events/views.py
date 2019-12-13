from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from mtm.settings import TZ, NAME
from .models import Location, Event, RecurringEvent

def index(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

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

def locations(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    q = request.GET.get('q', '')

    return render(request, 'events/location_dropdown.html',
        Location.objects.get_locations(request)
    )
