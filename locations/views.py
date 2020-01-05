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
from .models import Neighborhood, Location, CATEGORIES
from events.models import Event, RecurringEvent

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
        'API_KEY': API_KEY,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })
