import hashlib
import pytz
import re

from base64 import b16encode, b16decode
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from home.models import TimestampedModel
from mtm.settings import TZ, DOMAIN, INVITES_EXPIRY

class Invite(TimestampedModel):
    user = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.CASCADE)
    sent = models.BooleanField(default=False)
    _code = models.BinaryField(max_length=16, unique=True)

    @classmethod
    def create(cls):
        invite = cls.objects.create()

        hash_obj = hashlib.md5()
        hash_obj.update(str(invite.id).encode('utf-8'))
        invite._code = hash_obj.digest()

        invite.save()
        return invite

    @classmethod
    def get_invite_or_404(cls, code):
        return get_object_or_404(cls, _code=b16decode(code, casefold=True))

    @property
    def code(self):
        return str(b16encode(self._code).lower(), 'utf-8')

    @property
    def link(self):
        return '%s/invite/%s/' % (DOMAIN, self.code)

    @property
    def expiry_date(self):
        return self.date_created.astimezone(TZ) + INVITES_EXPIRY

    @property
    def expired(self):
        return self.expiry_date.astimezone(pytz.utc) < pytz.utc.localize(datetime.utcnow())
