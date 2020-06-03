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
        super().image_ops(relative_path=self.date_created.astimezone(TZ).strftime('authors/%Y/%m/%d/'), thumbnail_size=(200, 180))

    def delete(self, *args, **kwargs):
        if not AuthorImage.objects.filter(
            ~Q(id=self.id) &
            Q(date_created__date=self.date_created.date()) & (
                Q(_image_hash=self._image_hash) |
                Q(_thumbnail_hash=self._thumbnail_hash)
            )
        ):
            self.image.delete()
            self.thumbnail.delete()

        return super().delete(*args, **kwargs)

class Author(AbstractPerson):
    profile_image = models.ForeignKey(AuthorImage, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    bio = models.TextField(blank=True, null=True)

    def delete(self, *args, **kwargs):
        self.profile_image.delete()
        return super().delete(*args, **kwargs)

class Article(TimestampedModel, NewsItem):
    CATEGORY_CHOICES = [
        (0, 'Nightlife'),
        (1, 'Restaurants'),
        (3, 'Arts & Entertainment'),
        (4, 'Health & Fitness'),
        (5, 'Sports'),
        (6, 'Non-profit'),
        (7, 'Editorials & Opinions'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(default='', max_length=255, null=True, blank=True)
    body = models.TextField()
    album = models.ForeignKey(Album, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.PositiveSmallIntegerField(default=0, choices=CATEGORY_CHOICES)
    author = models.ForeignKey(Author, null=True, blank=True, on_delete=models.SET_NULL)
    objects = ArticleManager()

    def render(self, request):
        return render(request, 'articles/article_home.html', {
            'article': self,
        })

    def render_category(self, request):
        return render(request, 'articles/article_category.html', {
            'article': self,
        })

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.body = re.sub(r'(\r\n){2,}', '\r\n\r\n', self.body)

        super().save(*args, **kwargs)
