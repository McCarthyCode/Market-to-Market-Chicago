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

class Image(TimestampedModel):
    image = models.ImageField(default=None, upload_to='img/%Y/%m/%d/')
    _image_hash = models.BinaryField(editable=False, null=True, default=None, max_length=16)
    thumbnail = models.ImageField(editable=False, default=None, upload_to='img/%Y/%m/%d/')
    _thumbnail_hash = models.BinaryField(editable=False, null=True, default=None, max_length=16)
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

    def image_ops(self):
        self.generate_thumbnail()
        self.hash_thumbnail()
        self.resize_image()
        self.hash_image()

    def generate_thumbnail(self):
        img = PIL.Image.open(self.image).convert('RGB')
        width, height = img.size
        max_longest, max_shortest = 400, 360

        if (width >= height and (width > max_longest or height > max_shortest)) or (height > width and (height > max_longest or width > max_shortest)):
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

            new_name = re.sub(r'(img/\d{4}/\d{2}/\d{2}/)(.+)', r'thumbnail_\2', self.image.name.split('.')[0]) + '.jpg'
            self.thumbnail.save(new_name, img_file)

    def hash_thumbnail(self, block_size=65536):
        hasher = hashlib.md5()
        filename = MEDIA_ROOT + '/' + self.thumbnail.name

        with open(filename, 'rb') as f:
            for buf in iter(partial(f.read, block_size), b''):
                hasher.update(buf)

            if not self.thumbnail_hash or self.thumbnail_hash != hasher.hexdigest().lower():
                self._thumbnail_hash = hasher.digest()
                self.thumbnail.name = datetime.now().strftime('img/%Y/%m/%d/') + hasher.hexdigest().lower() + '.jpg'
                new_filename = MEDIA_ROOT + '/' + self.thumbnail.name
                os.rename(filename, new_filename)

    def resize_image(self):
        img = PIL.Image.open(self.image).convert('RGB')
        width, height = img.size
        max_longest, max_shortest = 960, 720

        if (width >= height and (width > max_longest or height > max_shortest)) or (height > width and (height > max_longest or width > max_shortest)):
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

            new_name = re.sub(r'(img/\d{4}/\d{2}/\d{2}/)(.+)', r'\2', self.image.name.split('.')[0]) + '.jpg'
            self.image.delete()
            self.image.save(new_name, img_file)

    def hash_image(self, block_size=65536):
        hasher = hashlib.md5()
        filename = MEDIA_ROOT + '/' + self.image.name

        with open(filename, 'rb') as f:
            for buf in iter(partial(f.read, block_size), b''):
                hasher.update(buf)

            if not self.image_hash or self.image_hash != hasher.hexdigest().lower():
                self._image_hash = hasher.digest()
                self.image.name = datetime.now().strftime('img/%Y/%m/%d/') + hasher.hexdigest().lower() + '.jpg'
                new_filename = MEDIA_ROOT + '/' + self.image.name
                os.rename(filename, new_filename)

    @property
    def image_hash(self):
        return str(b16encode(self._image_hash).lower(), 'utf-8') if self._image_hash else None

    @property
    def thumbnail_hash(self):
        return str(b16encode(self._thumbnail_hash).lower(), 'utf-8') if self._thumbnail_hash else None
