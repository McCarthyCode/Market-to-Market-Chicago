from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _

class ArticleManager(models.Manager):
    def delete(self, request, article):
        if article.album:
            delete_album = request.POST.get('delete-album', '')

            if delete_album == '':
                raise ValidationError(_('Please choose one of the album deletion options below.'), code='blank')
            elif delete_album == 'keep':
                article.delete()
            elif delete_album == 'delete':
                article.album.delete()
                article.delete()
            else:
                raise ValidationError(_('Invalid album deletion value. Please choose one of the options below.'), code='invalid')
        else:
            article.delete()
