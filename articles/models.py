from slugify import slugify
from titlecase import titlecase

from django.db import models

from home.models import TimestampedModel
from images.models import Album
from .managers import ArticleManager

class Article(TimestampedModel):
    CATEGORY_CHOICES = [
        (0, 'Nightlife'),
        (1, 'Restaurants'),
        (2, 'Arts & Entertainment'),
        (3, 'Health & Fitness'),
        (4, 'Sports'),
        (5, 'Non-profit'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(default='', max_length=255, null=True, blank=True)
    body = models.TextField()
    album = models.ForeignKey(Album, null=True, blank=True, on_delete=models.CASCADE)
    category = models.PositiveSmallIntegerField(default=0, choices=CATEGORY_CHOICES)
    objects = ArticleManager()

    def save(self, *args, **kwargs):
        self.title = titlecase(self.title.lower())
        self.slug = slugify(self.title)

        super().save(*args, **kwargs)
