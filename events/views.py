from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from mtm.settings import TZ, NAME
from .models import Event

def index(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'events/index.html', {
        'date': datetime.now(TZ),
        'calendar': Event.events.calendar_month(request),
        'name': NAME,
        'year': datetime.now(TZ).year,
    })
