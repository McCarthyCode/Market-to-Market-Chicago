from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth.models import User
from mtm.settings import TZ, NAME
from .models import Location, Event, RecurringEvent

def index(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    current_month = datetime.now(TZ).replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    return render(request, 'events/index.html', {
        'user': User.objects.get(pk=request.session['id']) \
            if 'id' in request.session else None,
        'calendar': Event.objects.calendar(request),
        'by_date': Event.objects.by_date(request),
        'by_location': Event.objects.by_location(request),
        'prev': current_month + relativedelta(months=-1),
        'next': current_month + relativedelta(months=+1),
        'name': NAME,
        'year': current_month.year,
    })

def month(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'events/month.html', {
        'calendar': Event.objects.calendar(request)
    })

def by_date(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'events/by_date.html', {
        'by_date': Event.objects.by_date(request)
    })

def by_location(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'events/by_location.html', {
        'by_location': Event.objects.by_location(request)
    })

def prev(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return JsonResponse(Event.objects.prev(request))

def next(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return JsonResponse(Event.objects.next(request))

def locations(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    q = request.GET.get('q', '')

    return render(request, 'events/location_dropdown.html',
        Location.objects.get_locations(request)
    )
