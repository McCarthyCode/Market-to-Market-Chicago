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
from events.models import Event

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

def location(request, name, id):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    try:
        location = Location.objects.get(id=id)
    except Location.DoesNotExist:
        return HttpResponseNotFound("Invalid location ID")

    _name = location.slug

    if location and _name != name:
        return HttpResponseRedirect(
            reverse('locations:location', args=[_name, id]))

    return render(request, 'locations/location.html', {
        'location': location,
        'events': Event.objects.filter(location=location)[:10],
        'name': NAME,
        'year': datetime.now(TZ).year,
        'API_KEY': API_KEY,
    })
