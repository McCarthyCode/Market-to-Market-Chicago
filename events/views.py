from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.contrib import messages
from django.http import (
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import render, redirect
from django.urls import reverse

from mtm.settings import TZ, NAME, API_KEY
from .models import Event

def index(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    current_month = datetime.now(TZ).replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    return render(request, 'events/index.html', {
        'user': request.user,
        'calendar': Event.objects.calendar(request),
        'by_date': Event.objects.by_date(request),
        'by_location': Event.objects.by_location(request),
        'prev': current_month + relativedelta(months=-1),
        'next': current_month + relativedelta(months=+1),
        'name': NAME,
        'year': current_month.year,
    })

def event(request, category, location_name, event_name, event_id):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    valid, response = Event.objects.event(category, location_name, event_name, event_id)

    if not valid:
        def invalid_id():
            return HttpResponseNotFound("Invalid event ID")

        def invalid_slug():
            return HttpResponseRedirect(
                reverse('events:event', args=response['args']))

        actions = {
            'invalid ID': invalid_id,
            'invalid slug': invalid_slug,
        }

        return actions[response['status']]()

    return render(request, 'events/event.html', {
        **response,
        'user': request.user,
        'name': NAME,
        'year': datetime.now(TZ).year,
        'API_KEY': API_KEY,
    })

def create_event(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    valid, response = Event.objects.create_event(request)

    if not valid:
        for error in response:
            messages.error(request, error)
    else:
        messages.success(request, response)

    return redirect('users:index')

def update_event(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    valid, response = Event.objects.update_event(request)

    if not valid:
        for error in response['errors']:
            messages.error(request, error)

        if response['event_found']:
            return redirect('events:event', *response['args'])
        else:
            return redirect('events:index')
    else:
        messages.success(request, response['success'])

    return redirect('events:event', *response['args'])

def delete_event(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    valid, response = Event.objects.delete_event(request)

    if not valid:
        for error in response['errors']:
            messages.error(request, error)

        if response['event_found']:
            return redirect('events:event', *response['args'])
        else:
            return redirect('events:index')
    else:
        messages.success(request, response['success'])

    return redirect('events:index')

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
