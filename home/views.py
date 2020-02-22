from datetime import datetime
from itertools import chain
from operator import attrgetter

from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

from articles.models import Article
# from events.models import Event
from images.models import Album, Image
from locations.models import Neighborhood, Location
from mtm.settings import TZ, NAME, ARTICLES_PER_PAGE, NEWS_ITEMS_PER_PAGE

def index(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    albums = []
    for album in Album.objects.all():
        if Image.objects.filter(album=album):
            albums.append(album)
    articles = Article.objects.all()
    # events = Event.objects.all()
    locations = Location.objects.all()

    feed = sorted(
        chain(
            albums,
            articles,
            # events,
            locations,
        ),
        key=attrgetter('date_updated'),
        reverse=True,
    )

    return render(request, 'home/index.html', {
        'title': 'Market to Market Chicago',
        'feed': feed[:NEWS_ITEMS_PER_PAGE],
        'user': request.user,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def about(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'home/about.html', {
        'title': 'About Market to Market Chicago',
        'user': request.user,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def category(request, slug):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    neighborhoods = Neighborhood.objects.all().order_by('name')
    locations_by_neighborhood = []

    slug_to_id = {
        'nightlife': 0,
        'restaurants': 1,
        'arts-and-entertainment': 2,
        'health-and-fitness': 3,
        'sports': 4,
        'non-profit': 5,
        'misc': 6,
    }

    slug_to_name = {
        'nightlife': 'Nightlife',
        'restaurants': 'Restaurants',
        'arts-and-entertainment': 'Arts & Entertainment','health-and-fitness': 'Health & Fitness',
        'sports': 'Sports',
        'non-profit': 'Non-profit',
        'misc': 'misc',
    }

    for neighborhood in neighborhoods:
        locations = Location.objects.filter(
            neighborhood=neighborhood,
            category=slug_to_id[slug],
        ).order_by('name')

        if locations:
            locations_by_neighborhood.append({
                'neighborhood': neighborhood,
                'locations': locations,
            })

    return render(request, 'home/category.html', {
        'title': slug_to_name[slug],
        'category_slug': slug,
        'locations_by_neighborhood': locations_by_neighborhood,
        'articles': Article.objects
            .filter(category=slug_to_id[slug])
            .order_by('-date_updated')[:ARTICLES_PER_PAGE],
        'show_category': False,
        'user': request.user,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def news_feed(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    page = request.GET.get('page', '')

    if not page:
        page = 1
    else:
        page = int(page)

    albums = []
    for album in Album.objects.all():
        if Image.objects.filter(album=album):
            albums.append(album)
    articles = Article.objects.all()
    # events = Event.objects.all()
    locations = Location.objects.all()

    feed = sorted(
        chain(
            albums,
            articles,
            # events,
            locations,
        ),
        key=attrgetter('date_updated'),
        reverse=True,
    )

    news_feed_paginator = Paginator(feed, NEWS_ITEMS_PER_PAGE)

    try:
        return render(request, 'home/news_feed.html', {
            'feed': news_feed_paginator.page(page).object_list,
        })
    except EmptyPage as exception:
        return HttpResponse(exception, status=204)
