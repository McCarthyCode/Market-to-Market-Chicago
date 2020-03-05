import hashlib
from base64 import b16encode

from django.db import models
from django.contrib.auth.models import User

from home.models import TimestampedModel
from mtm.settings import DOMAIN

class Invite(TimestampedModel):
    user = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.CASCADE)
    _code = models.BinaryField(max_length=16, unique=True)

    @classmethod
    def create(cls):
        invite = cls.objects.create()

        hash_obj = hashlib.md5()
        hash_obj.update(str(invite.id).encode('utf-8'))
        invite._code = hash_obj.digest()

        invite.save()
        return invite

    @property
    def code(self):
        return str(b16encode(self._code).lower(), 'utf-8')

    @property
    def link(self):
        return '%s/invite/?code=%s' % (DOMAIN, self.code)
