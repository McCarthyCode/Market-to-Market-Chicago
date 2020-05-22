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
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import render

from home.models import TimestampedModel, NewsItem
from .managers import AlbumManager, ImageManager
from mtm.settings import TZ, MEDIA_ROOT

class Album(TimestampedModel, NewsItem):
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
    category = models.PositiveSmallIntegerField(default=0, choices=CATEGORY_CHOICES)
    feed = models.BooleanField(default=False)
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

    def render_category(self, request):
        images = Image.objects.filter(album=self)

        return render(request, 'images/album_category.html', {
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

class ThumbnailedImage(TimestampedModel):
    image = models.ImageField(default=None, upload_to='img/%Y/%m/%d/')
    _image_hash = models.BinaryField(editable=False, null=True, default=None, max_length=16)
    thumbnail = models.ImageField(editable=False, default=None, upload_to='img/%Y/%m/%d/')
    _thumbnail_hash = models.BinaryField(editable=False, null=True, default=None, max_length=16)

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def __str__(self):
        return self.image.name

    def image_ops(
        self, relative_path=None, max_size=(960, 720), thumbnail_size=(400, 360),
    ):
        if relative_path == None:
            relative_path = self.date_created.astimezone(TZ).strftime('img/%Y/%m/%d/')

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

class Image(ThumbnailedImage):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    objects = ImageManager()

    def save(self, *args, **kwargs):
        self.album.date_updated = datetime.utcnow()
        self.album.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.album.date_updated = datetime.utcnow()
        self.album.save()

        if not Image.objects.filter(
            ~Q(id=self.id) &
            Q(date_created__date=self.date_created.date()) & (
                Q(_image_hash=self._image_hash) |
                Q(_thumbnail_hash=self._thumbnail_hash)
            )
        ):
            self.image.delete()
            self.thumbnail.delete()

        return super().delete(*args, **kwargs)

class AbstractPerson(TimestampedModel, NewsItem):
    slug = models.SlugField(max_length=70)
    prefix = models.CharField(blank=True, null=True, max_length=5)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    suffix = models.CharField(blank=True, null=True, max_length=5)
    bio = models.TextField()
    phone = models.CharField(blank=True, null=True, max_length=10)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    facebook = models.CharField(blank=True, null=True, max_length=70)
    twitter = models.CharField(blank=True, null=True, max_length=70)
    instagram = models.CharField(blank=True, null=True, max_length=70)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name)
        self.bio = re.sub(r'(\r\n){2,}', '\r\n', self.bio)

        super().save(*args, **kwargs)

    def render(self, request):
        return render(request, 'home/person_home.html', {
            'person': self,
        })

    @property
    def full_name(self):
        full_name = self.first_name + ' ' + self.last_name

        if self.prefix:
            full_name = self.prefix + ' ' + full_name

        if self.suffix:
            full_name = full_name + ' ' + self.suffix

        return full_name

    @property
    def display_phone(self):
        return '(%s) %s-%s' % \
            (self.phone[0:3], self.phone[3:6], self.phone[6:10]) \
            if self.phone else ''

    class Meta:
        abstract = True

class PersonImage(ThumbnailedImage):
    image = models.ImageField(blank=True, null=True, default=None, upload_to='people/%Y/%m/%d/')
    thumbnail = models.ImageField(editable=False, null=True, default=None, upload_to='people/%Y/%m/%d/')

    def image_ops(self):
        super().image_ops(relative_path=self.date_created.astimezone(TZ).strftime('people/%Y/%m/%d/'), thumbnail_size=(200, 180))

    def delete(self, *args, **kwargs):
        if not PersonImage.objects.filter(
            ~Q(id=self.id) &
            Q(date_created__date=self.date_created.date()) & (
                Q(_image_hash=self._image_hash) |
                Q(_thumbnail_hash=self._thumbnail_hash)
            )
        ):
            self.image.delete()
            self.thumbnail.delete()

        return super().delete(*args, **kwargs)

class Person(AbstractPerson):
    profile_image = models.ForeignKey(PersonImage, on_delete=models.SET_NULL, blank=True, null=True, default=None)

    def delete(self):
        self.profile_image.delete()
        return super().delete()

    class Meta:
        verbose_name_plural = 'people'
