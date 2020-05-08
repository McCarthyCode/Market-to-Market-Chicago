import re

from slugify import slugify

from django.db import models
from django.shortcuts import render

from home.models import TimestampedModel, NewsItem
from images.models import Album, ThumbnailedImage, AbstractPerson
from .managers import ArticleManager
from mtm.settings import TZ

class AuthorImage(ThumbnailedImage):
    image = models.ImageField(blank=True, null=True, default=None, upload_to='authors/%Y/%m/%d/')
    thumbnail = models.ImageField(editable=False, null=True, default=None, upload_to='authors/%Y/%m/%d/')

    def image_ops(self):
        super().image_ops(relative_path=self.date_created.astimezone(TZ).strftime('authors/%Y/%m/%d/'))

class Author(AbstractPerson):
    profile_image = models.ForeignKey(AuthorImage, on_delete=models.CASCADE, blank=True, null=True, default=None)
    bio = models.TextField(blank=True, null=True)

    def delete(self):
        self.profile_image.delete()
        return super().delete()

class Article(TimestampedModel, NewsItem):
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
    author = models.ForeignKey(Author, null=True, blank=True, on_delete=models.CASCADE)
    objects = ArticleManager()

    def render(self, request):
        return render(request, 'articles/article_home.html', {
            'article': self,
        })

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.body = re.sub(r'(\r\n){2,}', '\r\n\r\n', self.body)

        super().save(*args, **kwargs)
