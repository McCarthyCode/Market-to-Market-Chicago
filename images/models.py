from slugify import slugify
from django.db import models
from home.models import TimestampedModel
from .managers import AlbumManager, ImageManager

class Album(TimestampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(default='', max_length=255, null=True, blank=True)
    objects = AlbumManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Image(TimestampedModel):
    image = models.ImageField(upload_to='img/%Y/%m/%d/')
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    objects = ImageManager()
