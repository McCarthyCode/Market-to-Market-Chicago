from django.db import models
from home.models import TimestampedModel
from .managers import AlbumManager, ImageManager

class Album(TimestampedModel):
    title = models.CharField(max_length=200)
    objects = AlbumManager()

class Image(TimestampedModel):
    image = models.ImageField(upload_to='img/%Y/%m/%d/')
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    objects = ImageManager()
