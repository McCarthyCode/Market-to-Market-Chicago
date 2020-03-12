import hashlib
import os
import re

from base64 import b16encode
from functools import partial
from io import BytesIO
from PIL import Image

from django.db import models

from mtm.settings import TZ, MEDIA_ROOT

class TimestampedModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def updated_later(self):
        return self.date_updated.astimezone(TZ).replace(hour=0, minute=0, second=0, microsecond=0) > self.date_created.astimezone(TZ).replace(hour=0, minute=0, second=0, microsecond=0)

    class Meta:
        abstract = True

class NewsItem(TimestampedModel):
    def render(self, request):
        raise NotImplementedError('Subclasses of NewsItem must define their own render() method.')

    class Meta:
        abstract = True

class Person(NewsItem):
    prefix = models.CharField(blank=True, null=True, max_length=5)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    suffix = models.CharField(blank=True, null=True, max_length=5)
    image = models.ImageField(blank=True, null=True, default=None, upload_to='people/')
    _image_hash = models.BinaryField(editable=False, null=True, default=None, max_length=16)
    thumbnail = models.ImageField(editable=False, null=True, default=None, upload_to='people/')
    _thumbnail_hash = models.BinaryField(editable=False, null=True, default=None, max_length=16)
    bio = models.TextField()
    phone = models.CharField(blank=True, null=True, max_length=10)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.bio = re.sub(r'(\r\n){2,}', '\r\n', self.bio)

        super().save(*args, **kwargs)

    def image_ops(self):
        self.generate_thumbnail()
        self.hash_thumbnail()
        self.resize_image()
        self.hash_image()

    def generate_thumbnail(self):
        img = Image.open(self.image).convert('RGB')
        width, height = img.size
        max_longest, max_shortest = 300, 250

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

            img = img.resize((new_width, new_height), Image.ANTIALIAS)
            img_file = BytesIO()
            img.save(img_file, 'JPEG', quality=90)

            new_name = 'thumbnail_' + self.image.name.split('.')[0].replace('people/', '') + '.jpg'
            self.thumbnail.save(new_name, img_file)

    def hash_thumbnail(self, block_size=65536):
        hasher = hashlib.md5()
        filename = MEDIA_ROOT + '/' + self.thumbnail.name

        with open(filename, 'rb') as f:
            for buf in iter(partial(f.read, block_size), b''):
                hasher.update(buf)

            if not self.thumbnail_hash or self.thumbnail_hash != hasher.hexdigest().lower():
                self._thumbnail_hash = hasher.digest()
                self.thumbnail.name = 'people/' + hasher.hexdigest().lower() + '.jpg'
                new_filename = MEDIA_ROOT + '/' + self.thumbnail.name
                os.rename(filename, new_filename)

    def resize_image(self):
        img = Image.open(self.image).convert('RGB')
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

            img = img.resize((new_width, new_height), Image.ANTIALIAS)
            img_file = BytesIO()
            img.save(img_file, 'JPEG', quality=90)

            new_name = self.image.name.split('.')[0].replace('people/', '') + '.jpg'
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
                self.image.name = 'people/' + hasher.hexdigest().lower() + '.jpg'
                new_filename = MEDIA_ROOT + '/' + self.image.name
                os.rename(filename, new_filename)

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

    @property
    def image_hash(self):
        return str(b16encode(self._image_hash).lower(), 'utf-8') if self._image_hash else None

    @property
    def thumbnail_hash(self):
        return str(b16encode(self._thumbnail_hash).lower(), 'utf-8') if self._thumbnail_hash else None

    class Meta:
        verbose_name_plural = 'people'
