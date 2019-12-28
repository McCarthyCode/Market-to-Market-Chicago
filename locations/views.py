from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from mtm.settings import TZ, NAME
from .models import Neighborhood, Location

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

def location(request, id, slug):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    msg = 'slug: %s; id: %d' % (slug, int(id))

    return HttpResponse(msg, content_type='text/plain')
