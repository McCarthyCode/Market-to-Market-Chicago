from datetime import datetime

from django.contrib import messages
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.shortcuts import render, redirect
from django.urls import reverse

from mtm.settings import TZ, NAME, API_KEY
from .models import Neighborhood, Location, CATEGORIES
from events.models import Event, RecurringEvent
from .forms import CreateLocationForm

def neighborhood_autocomplete(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'home/autocomplete.html',
        Neighborhood.objects.autocomplete(request)
    )

def location_autocomplete(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'home/autocomplete.html',
        Location.objects.autocomplete(request)
    )

def neighborhood(request, slug, neighborhood_id):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    msg = 'slug: %s; id: %d' % (slug, int(neighborhood_id))

    return HttpResponse(msg, content_type='text/plain')

def location(request, category_slug, location_slug, location_id):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    valid, response = Location.objects.location(category_slug, location_slug, location_id)

    if not valid:
        def invalid_id():
            return HttpResponseNotFound("Invalid location ID")

        def invalid_slug():
            return HttpResponseRedirect(
                reverse('locations:location', args=response['args'])
            )

        actions = {
            'invalid ID': invalid_id,
            'invalid slug': invalid_slug,
        }

        return actions[response['status']]()

    return render(request, 'locations/location.html', {
        **response,
        'title': Location.objects.get(id=location_id).name,
        'user': request.user,
        'API_KEY': API_KEY,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def create_location(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    form = CreateLocationForm(request.POST)

    if form.is_valid():
        try:
            location = form.save()
        except ValidationError as error:
            messages.error(request, error)

            redirect('users:index')

        name = location.name
        punctuation = name[-1]
        messages.success(request, 'You have sucessfully created a location named "%s%s"' % (name, '' if punctuation == '?' or punctuation == '!' or punctuation == '.' else '.'))

        return redirect('locations:location',
            CATEGORIES[location.category], location.slug, location.id)

    messages.error(request, 'There was an error creating a location.')

    return redirect('users:index')

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
