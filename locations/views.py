from datetime import datetime

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import (
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.contrib import messages
from django.contrib.auth.models import User

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
    if request.method != 'GET':
        return HttpResponseBadRequest()

    valid, response = Location.objects.location(category, location_name, location_id)

    if not valid:
        def invalid_id():
            return HttpResponseNotFound("Invalid location ID")

        def invalid_slug():
            return HttpResponseRedirect(
                reverse('locations:location', args=response['args']))

        actions = {
            'invalid ID': invalid_id,
            'invalid slug': invalid_slug,
        }

        return actions[response['status']]()

    return render(request, 'locations/location.html', {
        **response,
        'user': User.objects.get(pk=request.session['id']) \
            if 'id' in request.session else None,
        'API_KEY': API_KEY,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def update_location(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    valid, response = Location.objects.update_location(request)

    if not valid:
        for error in response['errors']:
            messages.error(request, error)
    else:
        messages.success(request, response['success'])

    return redirect('locations:location', *response['args'])
