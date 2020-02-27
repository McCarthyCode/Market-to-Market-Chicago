from django.template.defaultfilters import slugify
from django.db import models
from django.shortcuts import render

from home.models import TimestampedModel, NewsItem
from .managers import NeighborhoodManager, LocationManager
from mtm.settings import TZ

CATEGORIES = [
    'nightlife',
    'restaurants',
    'nightlife-restaurants',
    'arts-and-entertainment',
    'health-and-fitness',
    'sports',
    'non-profit',
]

class Neighborhood(TimestampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(default='', editable=False, max_length=100, null=True, blank=True)
    objects = NeighborhoodManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Location(NewsItem):
    CATEGORY_CHOICES = [
        (0, 'Nightlife'),
        (1, 'Restaurants'),
        (2, 'Bar & Restaurant'),
        (3, 'Arts & Entertainment'),
        (4, 'Health & Fitness'),
        (5, 'Sports'),
        (6, 'Non-profit'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(default='', editable=False, max_length=100, null=True, blank=True)
    category = models.PositiveSmallIntegerField(choices=CATEGORY_CHOICES)
    neighborhood = models.ForeignKey(Neighborhood, null=True, blank=True, on_delete=models.SET_NULL)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(null=True, blank=True, max_length=200)
    city = models.CharField(max_length=80, default='Chicago')
    state = models.CharField(max_length=2, default='IL')
    zip_code = models.CharField(null=True, blank=True, max_length=5)
    website = models.URLField(null=True, blank=True)
    phone = models.CharField(null=True, blank=True, max_length=10)
    override_slug = models.BooleanField(default=False)
    objects = LocationManager()

    def category_slug(self):
        slugs = [
            'nightlife',
            'restaurants',
            'arts-and-entertainment',
            'health-and-fitness',
            'sports',
            'non-profit',
        ]

        return slugs[self.category]

    def display_phone(self):
        return '(%s) %s-%s' % \
            (self.phone[0:3], self.phone[3:6], self.phone[6:10]) \
            if self.phone else ''

    def render(self, request):
        return render(request, 'locations/location_home.html', {
            'location': self,
        })

    def save(self, *args, **kwargs):
        self.address1 = self.address1.replace('.', '')
        self.address2 = self.address2.replace('.', '')

        if not self.override_slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
