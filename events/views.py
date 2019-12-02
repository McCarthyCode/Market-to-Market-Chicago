from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from mtm.settings import TZ, NAME
from .models import Event

def index(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    calendar_month = Event.events.calendar_month(request)

    return render(request, 'events/index.html', {
        **Event.events.calendar_month(request),
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def month(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'events/month.html', Event.events.calendar_month(request))

def prev(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'events/month.html', Event.events.prev(request))

def next(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'events/month.html', Event.events.next(request))
