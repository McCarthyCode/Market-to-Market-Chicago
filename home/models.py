import hashlib
import os
import re

from base64 import b16encode
from functools import partial
from io import BytesIO
from PIL import Image

from django.db import models
from django.shortcuts import render

from mtm.settings import TZ, MEDIA_ROOT

class TimestampedModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def updated_later(self):
        return self.date_updated.astimezone(TZ).replace(hour=0, minute=0, second=0, microsecond=0) > self.date_created.astimezone(TZ).replace(hour=0, minute=0, second=0, microsecond=0)

    class Meta:
        abstract = True

class NewsItem(models.Model):
    def render(self, request):
        raise NotImplementedError('Subclasses of NewsItem must define their own render() method.')

    class Meta:
        abstract = True
