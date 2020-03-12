import random

from datetime import datetime
from itertools import chain
from operator import attrgetter

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404

from .models import NewsItem, Person
from users.models import Invite
from articles.models import Article
from images.models import Album, Image
from locations.models import Neighborhood, Location

from .forms import CreatePersonForm
from users.forms import CreateInvitesForm, RegistrationForm
from locations.forms import CreateLocationForm
from articles.forms import CreateArticleForm

from mtm.settings import TZ, NAME, ARTICLES_PER_PAGE, NEWS_ITEMS_PER_PAGE, MAX_INVITES

def index(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    albums = []
    for album in Album.objects.all():
        if Image.objects.filter(album=album):
            albums.append(album)

    articles = Article.objects.all()

    locations = Location.objects.all()

    feed = sorted(
        chain(
            albums,
            articles,
            locations,
        ),
        key=attrgetter('date_updated'),
        reverse=True,
    )

    ads_order = list(range(3))
    random.shuffle(ads_order)

    return render(request, 'home/index.html', {
        'title': 'Market to Market Chicago',
        'feed': feed[:NEWS_ITEMS_PER_PAGE],
        'ads_order': ads_order,
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
        'people': Person.objects.all().order_by('-date_updated'),
        'user': request.user,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def create_person(request):
    if not request.user.is_superuser or request.method != 'POST':
        return HttpResponseBadRequest()

    form = CreatePersonForm(request.POST, request.FILES)

    if form.is_valid():
        person = form.save()
        person.prefix = form.cleaned_data.get('prefix')
        person.first_name = form.cleaned_data.get('first_name')
        person.last_name = form.cleaned_data.get('last_name')
        person.suffix = form.cleaned_data.get('suffix')
        person.bio = form.cleaned_data.get('bio')
        person.phone = form.cleaned_data.get('phone')
        person.email = form.cleaned_data.get('email')

        if 'image' in request.FILES:
            person.image_ops()

        person.save()

        messages.success(request, 'You have successfully created a person to know.')

        return redirect('users:index')

    messages.error(request, 'There was an error creating a person to know.')

    if request.user.is_superuser:
        return render(request, 'users/index.html', {
            'create_article_form': CreateArticleForm(),
            'create_person_form': CreatePersonForm(request.POST),
            'create_invites_form': CreateInvitesForm(),
            'invites': [x for x in Invite.objects.filter(sent=False).order_by('date_created') if not x.expired][:MAX_INVITES],
            'create_location_form': CreateLocationForm(),
            'user': request.user,
            'name': NAME,
            'year': datetime.now(TZ).year,
        })

    return render(request, 'users/index.html', {
        'create_location_form': CreateLocationForm(),
        'user': request.user,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def update_person(request, person_id):
    if not request.user.is_superuser:
        return HttpResponseBadRequest()

    person = get_object_or_404(Person, id=person_id)

    if request.method == 'GET':
        return render(request, 'home/update_person.html', {
            'person': person,
            'form': CreatePersonForm(instance=person),
            'title': 'Update %s' % person.full_name,
            'user': request.user,
            'name': NAME,
            'year': datetime.now(TZ).year,
        })
    elif request.method == 'POST':
        person.image.delete()
        person.thumbnail.delete()

        form = CreatePersonForm(request.POST, request.FILES, instance=person)

        if form.is_valid():
            updated_person = form.save()
            updated_person.prefix = form.cleaned_data.get('prefix')
            updated_person.first_name = form.cleaned_data.get('first_name')
            updated_person.last_name = form.cleaned_data.get('last_name')
            updated_person.suffix = form.cleaned_data.get('suffix')
            updated_person.bio = form.cleaned_data.get('bio')
            updated_person.phone = form.cleaned_data.get('phone')
            updated_person.email = form.cleaned_data.get('email')
            updated_person._image_hash = None
            updated_person._thumbnail_hash = None

            if 'image' in request.FILES:
                updated_person.image_ops()

            updated_person.save()

            messages.success(request, 'You have successfully updated %s.' % person.full_name)
        else:
            messages.error(request, 'There was an error updating %s.' % person.full_name)

            return render(request, 'home/update_person.html', {
                'person': person,
                'form': form,
                'title': '',
                'user': request.user,
                'name': NAME,
                'year': datetime.now(TZ).year,
            })
    else:
        return HttpResponseBadRequest()

    return redirect('home:people-to-know')

def delete_person(request, person_id):
    if not request.user.is_superuser or request.method != 'GET':
        return HttpResponseBadRequest()

    person = get_object_or_404(Person, id=person_id)

    name = person.full_name
    person.image.delete()
    person.thumbnail.delete()
    person.delete()

    messages.success(request, 'You have successfully deleted %s.' % name)

    return redirect('home:people-to-know')

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
    ads_order = request.GET.get('ads-order', '[0, 1, 2]')

    if not page:
        page = 1
    else:
        page = int(page)

    ads_order = ads_order.replace('[', '').replace(']', '').replace(',', '')
    ads_order = ads_order.split(' ')
    ads_order = [int(i) for i in ads_order]

    albums = []
    for album in Album.objects.all():
        if Image.objects.filter(album=album):
            albums.append(album)
    articles = Article.objects.all()
    locations = Location.objects.all()

    feed = sorted(
        chain(
            albums,
            articles,
            locations,
        ),
        key=attrgetter('date_updated'),
        reverse=True,
    )

    news_feed_paginator = Paginator(feed, NEWS_ITEMS_PER_PAGE)

    try:
        return render(request, 'home/news_feed.html', {
            'feed': news_feed_paginator.page(page).object_list,
            'ads_order': ads_order,
        })
    except EmptyPage as exception:
        return HttpResponse(exception, status=204)
