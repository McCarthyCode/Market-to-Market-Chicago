from datetime import datetime
from slugify import slugify

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render

from home.models import TimestampedModel, NewsItem
from .managers import AlbumManager, ImageManager

class Album(NewsItem):
    title = models.CharField(max_length=255)
    slug = models.SlugField(default='', max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = AlbumManager()

    def render(self, request):
        images = Image.objects.filter(album=self)

        return render(request, 'images/album_home.html', {
            'album': self,
            'images': images,
            'image_preview': images[:5] if len(images) > 6 else images,
        })

    @property
    def date_album_images_updated(self):
        latest_change = self.date_updated

        for image in Image.objects.filter(album=self):
            if image.date_updated > latest_change:
                latest_change = image.date_updated

        return latest_change

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Image(TimestampedModel):
    image = models.ImageField(upload_to='img/%Y/%m/%d/')
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    objects = ImageManager()

    def save(self, *args, **kwargs):
        self.album.date_updated = datetime.utcnow()
        self.album.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.album.date_updated = datetime.utcnow()
        self.album.save()

        super().delete(*args, **kwargs)
