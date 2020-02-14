from slugify import slugify

from django.db import models
from django.contrib.auth.models import User

from home.models import TimestampedModel, NewsItem
from .managers import AlbumManager, ImageManager

class Album(NewsItem):
    title = models.CharField(max_length=255)
    slug = models.SlugField(default='', max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = AlbumManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Image(TimestampedModel):
    image = models.ImageField(upload_to='img/%Y/%m/%d/')
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    objects = ImageManager()
