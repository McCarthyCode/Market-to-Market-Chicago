from datetime import datetime
from itertools import chain
from operator import attrgetter

from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

from .models import NewsItem
from articles.models import Article
# from events.models import Event, RecurringEvent
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

    # events = []
    # _events = Event.objects.filter(date_start__gte=datetime.utcnow()).order_by('date_start')[:5]
    # recurring_events_info = []
    # for event in _events:
    #     print(event.__class__)
    #     if event.__class__.__base__ == Event:
    #         events.append(event)
    #     elif event.__class__.__base__ == RecurringEvent:
    #         events.append(event)
    #     elif event.__class__.__base__ == NewsItem:
    #         events.append(event)

    #         # if event.info not in recurring_events_info:
    #         #     recurring_event = RecurringEvent.objects.filter(date_start__gte=datetime.utcnow(), info=event.info).order_by('-date_start').first()
    #         #     events.append(recurring_event)
    #         #     recurring_events_info.append(event.info)

    locations = Location.objects.all()

    feed = sorted(
        chain(
            albums,
            articles,
            # _events,
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

def people(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'home/people.html', {
        'title': 'People to Know',
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
        'arts-and-entertainment': 3,
        'health-and-fitness': 4,
        'sports': 5,
        'non-profit': 6,
    }

    slug_to_name = {
        'nightlife': 'Nightlife',
        'restaurants': 'Restaurants',
        'arts-and-entertainment': 'Arts & Entertainment','health-and-fitness': 'Health & Fitness',
        'sports': 'Sports',
        'non-profit': 'Non-profit',
    }

    for neighborhood in neighborhoods:
        category_id = slug_to_id[slug]

        if category_id == 0 or category_id == 1:
            locations = Location.objects.filter(
                Q(category=category_id) | Q(category=2),
                neighborhood=neighborhood,
            ).order_by('name')
        else:
            locations = Location.objects.filter(
                neighborhood=neighborhood,
                category=category_id,
            ).order_by('name')

        if locations:
            locations_by_neighborhood.append({
                'neighborhood': neighborhood,
                'locations': locations,
            })

    def len_locations(obj):
        return len(obj['locations'])

    return render(request, 'home/category.html', {
        'title': slug_to_name[slug],
        'category_slug': slug,
        'locations_by_neighborhood': sorted(locations_by_neighborhood, key=len_locations, reverse=True),
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
