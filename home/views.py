import os
import random

from datetime import datetime
from itertools import chain
from operator import attrgetter

from django.contrib import messages
from django.core.files import File
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.shortcuts import render, redirect, get_object_or_404

from .models import NewsItem
from users.models import Invite
from articles.models import Article
from images.models import Album, Image, Person, PersonImage
from locations.models import Neighborhood, Location

from .forms import PersonForm
from users.forms import InvitesForm, RegistrationForm
from locations.forms import LocationForm
from articles.forms import AuthorForm, ArticleForm

from mtm.settings import (
    TZ,
    NAME,
    NEWS_ITEMS_PER_PAGE,
    MAX_INVITES,
    MEDIA_ROOT
)

def handler400(request, exception=None):
    return render(request, 'home/errors/400.html', status=200)

def handler403(request, exception=None):
    return render(request, 'home/errors/403.html', status=200)

def handler404(request, exception=None):
    return render(request, 'home/errors/404.html', status=200)

def handler500(request, exception=None):
    return render(request, 'home/errors/500.html', status=200)

def index(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    albums = []
    for album in Album.objects.filter(feed=True):
        if Image.objects.filter(album=album):
            albums.append(album)

    articles = Article.objects.all()
    locations = Location.objects.all()
    people = Person.objects.all()

    feed = sorted(
        chain(
            albums,
            articles,
            locations,
            people,
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
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def about(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'home/about.html', {
        'title': 'About Market to Market Chicago',
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def people(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    return render(request, 'home/people.html', {
        'title': 'People to Know',
        'people': Person.objects.all().order_by('-date_updated'),
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def create_person(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    if not request.user.is_superuser:
        return HttpResponseForbidden()

    form = PersonForm(request.POST, request.FILES)

    if form.is_valid():
        person = form.save(commit=False)

        if 'image' in request.FILES:
            profile_image = PersonImage.objects.create(image=request.FILES.get('image'))
            profile_image.image_ops()
            profile_image.save()
            person.profile_image = profile_image

        person.save()

        full_name = person.full_name
        punctuation = full_name[-1]
        messages.success(request, 'You have successfully created a person to know named "%s%s"' % (full_name, '' if punctuation == '?' or punctuation == '!' or punctuation == '.' else '.'))

        return redirect('users:index')

    messages.error(request, 'There was an error creating a person to know.')

    if request.user.is_superuser:
        return render(request, 'users/index.html', {
            'create_person_form': PersonForm(request.POST),
            'create_author_form': AuthorForm(),
            'create_article_form': ArticleForm(),
            'create_invites_form': InvitesForm(),
            'invites': [x for x in Invite.objects.filter(sent=False).order_by('date_created') if not x.expired][:MAX_INVITES],
            'create_location_form': LocationForm(),
            'create_album_form': CreateAlbumForm(),
            'name': NAME,
            'year': datetime.now(TZ).year,
        })

    return render(request, 'users/index.html', {
        'create_location_form': LocationForm(),
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def update_person(request, person_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    person = get_object_or_404(Person, id=person_id)

    if request.method == 'GET':
        return render(request, 'home/update_person.html', {
            'person': person,
            'form': PersonForm(instance=person),
            'title': 'Update %s' % person.full_name,
            'name': NAME,
            'year': datetime.now(TZ).year,
        })
    elif request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=person)

        if form.is_valid():
            if 'image' in request.FILES and person.profile_image:
                # only delete image if hash exists and image is not being used elsewhere
                if not Person.objects.filter(
                    ~Q(id=person.id) & (
                        Q(profile_image___image_hash=person.profile_image._image_hash) |
                        Q(profile_image___thumbnail_hash=person.profile_image._image_hash)
                    )
                ) and person.profile_image._image_hash:
                    filename = '%s/people/%s/%s.jpg' % (MEDIA_ROOT, person.profile_image.date_created.astimezone(TZ).strftime('%Y/%m/%d'), person.profile_image.image_hash)
                    os.remove(filename)

                # only delete thumbnail if hash exists and image is not being used elsewhere
                if Person.objects.filter(
                    ~Q(id=person.id) & (
                        Q(profile_image___image_hash=person.profile_image._thumbnail_hash) |
                        Q(profile_image___thumbnail_hash=person.profile_image._thumbnail_hash)
                    )
                ) and person.profile_image.thumbnail_hash:
                    person.profile_image.thumbnail = None
                else:
                    person.profile_image.thumbnail.delete()

                person.profile_image._image_hash = None
                person.profile_image._thumbnail_hash = None

                person.save()

            updated_person = form.save()

            if 'image' in request.FILES:
                profile_image = PersonImage.objects.create(image=request.FILES.get('image'))
                profile_image.image_ops()
                profile_image.save()
                updated_person.profile_image = profile_image
            elif form.cleaned_data.get('clear_image'):
                updated_person.profile_image.delete()
                updated_person.profile_image.save()
                updated_person.profile_image = None

            updated_person.save()

            messages.success(request, 'You have successfully updated %s.' % person.full_name)
        else:
            messages.error(request, 'There was an error updating %s.' % person.full_name)

            return render(request, 'home/update_person.html', {
                'person': person,
                'form': form,
                'title': '',
                'name': NAME,
                'year': datetime.now(TZ).year,
            })
    else:
        return HttpResponseBadRequest()

    return redirect('home:people-to-know')

def delete_person(request, person_id):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    if not request.user.is_superuser:
        return HttpResponseForbidden()

    person = get_object_or_404(Person, id=person_id)

    name = person.full_name
    person.delete()

    messages.success(request, 'You have successfully deleted %s.' % name)

    return redirect('home:people-to-know')

def category(request, slug):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    neighborhoods = [] if slug == 'editorials-and-opinions' else Neighborhood.objects.all().order_by('name')
    locations_by_neighborhood = []

    slug_to_id = {
        'nightlife': 0,
        'restaurants': 1,
        'arts-and-entertainment': 3,
        'health-and-fitness': 4,
        'sports': 5,
        'non-profit': 6,
        'editorials-and-opinions': 7,
    }

    slug_to_name = {
        'nightlife': 'Nightlife',
        'restaurants': 'Restaurants',
        'arts-and-entertainment': 'Arts & Entertainment',
        'health-and-fitness': 'Health & Fitness',
        'sports': 'Sports',
        'non-profit': 'Non-profit',
        'editorials-and-opinions': 'Editorials & Opinions',
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


    albums = []
    for album in Album.objects.filter(feed=True, category=slug_to_id[slug])[:NEWS_ITEMS_PER_PAGE]:
        if Image.objects.filter(album=album):
            albums.append(album)

    articles = Article.objects.filter(category=slug_to_id[slug])[:NEWS_ITEMS_PER_PAGE]

    feed = sorted(
        chain(
            albums,
            articles,
        ),
        key=attrgetter('date_updated'),
        reverse=True,
    )[:NEWS_ITEMS_PER_PAGE]

    def len_locations(obj):
        return len(obj['locations'])

    return render(request, 'home/category.html', {
        'title': slug_to_name[slug],
        'category_slug': slug,
        'locations_by_neighborhood': [] if slug == 'editorials-and-opinions' else sorted(locations_by_neighborhood, key=len_locations, reverse=True),
        'feed': feed,
        'show_category': False,
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

def category_feed(request, slug, page):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    page = int(page)

    slug_to_id = {
        'nightlife': 0,
        'restaurants': 1,
        'arts-and-entertainment': 3,
        'health-and-fitness': 4,
        'sports': 5,
        'non-profit': 6,
        'editorials-and-opinions': 7,
    }

    albums = []
    for album in Album.objects.filter(feed=True, category=slug_to_id[slug])[:NEWS_ITEMS_PER_PAGE]:
        if Image.objects.filter(album=album):
            albums.append(album)

    articles = Article.objects.filter(category=slug_to_id[slug])[:NEWS_ITEMS_PER_PAGE]

    feed = sorted(
        chain(
            albums,
            articles,
        ),
        key=attrgetter('date_updated'),
        reverse=True,
    )

    feed_paginator = Paginator(feed, NEWS_ITEMS_PER_PAGE)

    try:
        return render(request, 'home/category_feed.html', {
            'feed': feed_paginator.page(page).object_list,
        })
    except EmptyPage as exception:
        return HttpResponse(exception, status=204)
