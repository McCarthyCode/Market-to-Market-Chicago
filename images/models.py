import hashlib
import os
import PIL
import re

from base64 import b16encode
from datetime import datetime
from functools import partial
from io import BytesIO
from slugify import slugify

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render

from home.models import TimestampedModel, NewsItem
from .managers import AlbumManager, ImageManager
from mtm.settings import MEDIA_ROOT

class Album(NewsItem):
    title = models.CharField(max_length=255)
    slug = models.SlugField(default='', max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = AlbumManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def render(self, request):
        images = Image.objects.filter(album=self)

        return render(request, 'images/album_home.html', {
            'album': self,
            'images': images,
            'images_preview': images[:5] if len(images) > 6 else images,
        })

    @property
    def date_album_images_updated(self):
        latest_change = self.date_updated

        for image in Image.objects.filter(album=self):
            if image.date_updated > latest_change:
                latest_change = image.date_updated

        return latest_change

class ThumbnailedImage(models.Model):
    image = models.ImageField(default=None, upload_to='img/%Y/%m/%d/')
    _image_hash = models.BinaryField(editable=False, null=True, default=None, max_length=16)
    thumbnail = models.ImageField(editable=False, default=None, upload_to='img/%Y/%m/%d/')
    _thumbnail_hash = models.BinaryField(editable=False, null=True, default=None, max_length=16)

    @classmethod
    def create(cls, *args, **kwargs):
        image = cls(**kwargs)
        image.image_ops()

        return image

    def __str__(self):
        return self.image.name

    def image_ops(
        self, relative_path=None, max_size=(960, 720), thumbnail_size=(400, 360),
    ):
        if relative_path == None:
            relative_path = self.date_created.strftime('img/%Y/%m/%d')

        self._generate_thumbnail(relative_path, thumbnail_size)
        self._hash_thumbnail(relative_path)
        self._resize_image(relative_path, max_size)
        self._hash_image(relative_path)

    def _generate_thumbnail(self, relative_path, thumbnail_size):
        img = PIL.Image.open(self.image).convert('RGB')
        width, height = img.size
        max_longest, max_shortest = thumbnail_size

        if not self.thumbnail and (width >= height and (width > max_longest or height > max_shortest)) or (height > width and (height > max_longest or width > max_shortest)):
            if width > height:
                if (height * max_longest/ width) > max_shortest:
                    new_height = max_shortest
                    new_width = int(width * new_height / height)
                else:
                    new_width = max_longest
                    new_height = int(height * new_width / width)
            else:
                if (width * max_longest / height) > max_shortest:
                    new_width = max_shortest
                    new_height = int(height * new_width / width)
                else:
                    new_height = max_longest
                    new_width = int(width * new_height / height)

            img = img.resize((new_width, new_height), PIL.Image.ANTIALIAS)

        img_file = BytesIO()
        img.save(img_file, 'JPEG', quality=90)

        new_name = 'thumbnail_' + self.image.name.split('.')[0].replace(relative_path, '') + '.jpg'
        self.thumbnail.save(new_name, img_file)

    def _hash_thumbnail(self, relative_path, block_size=65536):
        hasher = hashlib.md5()
        filename = MEDIA_ROOT + '/' + self.thumbnail.name

        with open(filename, 'rb') as f:
            for buf in iter(partial(f.read, block_size), b''):
                hasher.update(buf)

            if not self.thumbnail_hash or self.thumbnail_hash != hasher.hexdigest().lower():
                self._thumbnail_hash = hasher.digest()
                self.thumbnail.name = relative_path + hasher.hexdigest().lower() + '.jpg'
                new_filename = MEDIA_ROOT + '/' + self.thumbnail.name
                os.rename(filename, new_filename)

    def _resize_image(self, relative_path, max_size):
        img = PIL.Image.open(self.image).convert('RGB')
        width, height = img.size
        max_width, max_height = max_size

        if (width >= height and (width > max_width or height > max_height)) or (height > width and (height > max_height or width > max_width)):
            if width > height:
                if (height * max_width/ width) > max_height:
                    new_height = max_height
                    new_width = int(width * new_height / height)
                else:
                    new_width = max_width
                    new_height = int(height * new_width / width)
            else:
                if (width * max_width / height) > max_height:
                    new_width = max_height
                    new_height = int(height * new_width / width)
                else:
                    new_height = max_width
                    new_width = int(width * new_height / height)

            img = img.resize((new_width, new_height), PIL.Image.ANTIALIAS)

        img_file = BytesIO()
        img.save(img_file, 'JPEG', quality=90)

        new_name = self.image.name.split('.')[0].replace(relative_path, '') + '.jpg'
        self.image.delete()
        self.image.save(new_name, img_file)

    def _hash_image(self, relative_path, block_size=65536):
        hasher = hashlib.md5()
        filename = MEDIA_ROOT + '/' + self.image.name

        with open(filename, 'rb') as f:
            for buf in iter(partial(f.read, block_size), b''):
                hasher.update(buf)

            if not self.image_hash or self.image_hash != hasher.hexdigest().lower():
                self._image_hash = hasher.digest()
                self.image.name = relative_path + hasher.hexdigest().lower() + '.jpg'
                new_filename = MEDIA_ROOT + '/' + self.image.name
                os.rename(filename, new_filename)

    @property
    def image_hash(self):
        return str(b16encode(self._image_hash).lower(), 'utf-8') if self._image_hash else None

    @property
    def thumbnail_hash(self):
        return str(b16encode(self._thumbnail_hash).lower(), 'utf-8') if self._thumbnail_hash else None

    class Meta:
        abstract = True

class Image(TimestampedModel, ThumbnailedImage):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.album.date_updated = datetime.utcnow()
        self.album.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.album.date_updated = datetime.utcnow()
        self.album.save()

        super().delete(*args, **kwargs)
