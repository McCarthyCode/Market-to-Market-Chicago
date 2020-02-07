from datetime import datetime

from django.http import HttpResponseBadRequest
from django.shortcuts import render

from locations.models import Location
from mtm.settings import TZ, NAME

def index(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'home/index.html', {
        'user': request.user,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def category(request, slug):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    slug_to_title = {
        'nightlife': 'Nightlife',
        'restaurants': 'Restaurants',
        'arts-and-entertainment': 'Arts & Entertainment','health-and-fitness': 'Health & Fitness',
        'sports': 'Sports',
        'non-profit': 'Non-profit',
        'misc': 'misc',
    }

    return render(request, 'home/category.html', {
        'category': slug_to_title[slug],
        'user': request.user,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })
