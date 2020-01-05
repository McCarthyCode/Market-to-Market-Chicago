from django.template.defaultfilters import slugify
from django.db import models
from home.models import TimestampedModel
from .managers import NeighborhoodManager, LocationManager
from mtm.settings import TZ

CATEGORIES = [
    'nightlife',
    'restaurants',
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

class Location(TimestampedModel):
    CATEGORY_CHOICES = [
        (0, 'Nightlife'),
        (1, 'Restaurants'),
        (2, 'Arts & Entertainment'),
        (3, 'Health & Fitness'),
        (4, 'Sports'),
        (5, 'Non-profit'),
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
    objects = LocationManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
