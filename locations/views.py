from datetime import datetime
from django.shortcuts import render
from django.urls import reverse
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseRedirect,
    JsonResponse,
)
from mtm.settings import TZ, NAME, API_KEY
from .models import Neighborhood, Location
from events.models import Event, RecurringEvent

CATEGORIES = [
    'nightlife',
    'restaurants',
    'arts-and-entertainment',
    'health-and-fitness',
    'sports',
    'non-profit',
]

def neighborhoods_autocomplete(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'locations/autocomplete.html',
        Neighborhood.objects.neighborhoods_autocomplete(request)
    )

def locations_autocomplete(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'locations/autocomplete.html',
        Location.objects.locations_autocomplete(request)
    )

def neighborhood(request, id, slug):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    msg = 'slug: %s; id: %d' % (slug, int(id))

    return HttpResponse(msg, content_type='text/plain')

def location(request, category, location_name, location_id):
    print('location()')
    if request.method != 'GET':
        return HttpResponseBadRequest()

    try:
        location = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        return HttpResponseNotFound("Invalid location ID")

    _category = CATEGORIES[location.category]
    _location_name = location.slug

    if _category != category or _location_name != location_name:
        return HttpResponseRedirect(
            reverse(
                'locations:location',
                args=[_category, _location_name, location_id]
            )
        )

    events = Event.objects.filter(
        location=location,
        date_start__gte=datetime.now(TZ).replace(
            hour=0, minute=0, second=0, microsecond=0),
    ).order_by('date_start')[:10]

    return render(request, 'locations/location.html', {
        'location': location,
        'events': events,
        'category': _category,
        'name': NAME,
        'year': datetime.now(TZ).year,
        'API_KEY': API_KEY,
        'CATEGORIES': CATEGORIES,
    })

def event(request, category, location_name, event_name, event_id):
    print('event()')
    if request.method != 'GET':
        return HttpResponseBadRequest()

    try:
        event = RecurringEvent.objects.get(id=event_id)
        recurring = True
    except RecurringEvent.DoesNotExist:
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return HttpResponseNotFound("Invalid event ID")

        recurring = False

    _category = CATEGORIES[event.location.category]
    _location_name = event.location.slug
    _event_name = event.slug

    if _category != category or \
        _location_name != location_name or \
        _event_name != event_name:
        return HttpResponseRedirect(
            reverse(
                'locations:event',
                args=[_category, _location_name, _event_name, event_id]
            )
        )

    if recurring:
        next_event = RecurringEvent.objects.filter(
            first_occurence=event.first_occurence,
            date_start__gt=event.date_start,
        ).order_by('date_start').first()
    else:
        next_event = None

    return render(request, 'events/event.html', {
        'event': event,
        'next_event': next_event,
        'category': _category,
        'name': NAME,
        'year': datetime.now(TZ).year,
        'API_KEY': API_KEY,
    })
