from datetime import datetime

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from mtm.settings import TZ, NAME, GOOGLE_MAPS_API_KEY
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

def neighborhood(request, neighborhood_slug, neighborhood_id):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    neighborhood = Neighborhood.objects.get(id=neighborhood_id)

    return render(request, 'locations/neighborhood.html', {
        'title': neighborhood.name,
        'events': Event.objects.filter(location__neighborhood=neighborhood, date_start__gte=datetime.utcnow()).order_by('date_start')[:10],
        'locations': Location.objects.filter(neighborhood=neighborhood).order_by('name'),
        'neighborhood': neighborhood,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

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

    location = Location.objects.get(id=location_id)
    name = location.name
    category = location.category

    if response['no_kitchen'] and category == 2:
        messages.info(request, '%s does not have a kitchen but is listed as a restaurant because outside food is allowed.' % name)

    return render(request, 'locations/location.html', {
        **response,
        'title': name,
        'update_location_form': CreateLocationForm(instance=location),
        'user': request.user,
        'GOOGLE_MAPS_API_KEY': GOOGLE_MAPS_API_KEY,
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

def update_location(request, category_slug, location_slug, location_id):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    location = get_object_or_404(Location, pk=location_id)

    form = CreateLocationForm(request.POST)
    if form.is_valid():
        location.name = form.cleaned_data['name']
        location.category = form.cleaned_data['category']
        location.neighborhood = form.cleaned_data['neighborhood']
        location.address1 = form.cleaned_data['address1']
        location.address2 = form.cleaned_data['address2']
        location.city = form.cleaned_data['city']
        location.state = form.cleaned_data['state']
        location.zip_code = form.cleaned_data['zip_code']
        location.website = form.cleaned_data['website']
        location.phone = form.cleaned_data['phone']
        location.no_kitchen = form.cleaned_data['no_kitchen']

        location.save()

        name = location.name
        punctuation = name[-1]
        messages.success(request, 'You have sucessfully updated "%s%s"' % (name, '' if punctuation == '?' or punctuation == '!' or punctuation == '.' else '.'))
    else:
        name = location.name
        punctuation = name[-1]
        messages.error(request, 'There was an error updating "%s%s"' % (name, '' if punctuation == '?' or punctuation == '!' or punctuation == '.' else '.'))

    return redirect('locations:location', location.category_slug(), location.slug, location_id)

def delete_location(request, category_slug, location_slug, location_id):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    location = Location.objects.get(id=location_id)
    name = location.name
    Event.objects.filter(location=location).delete()
    location.delete()

    punctuation = name[-1]
    messages.success(request, 'You have sucessfully deleted the location "%s%s"' % (name, '' if punctuation == '?' or punctuation == '!' or punctuation == '.' else '.'))

    return redirect('users:index')
