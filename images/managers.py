import magic

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _

class AlbumManager(models.Manager):
    def upload_images(self, album, images):
        from .models import Image

        for image in images:
            # Check MIME Content-Type before saving
            filetype = magic.from_buffer(image.read(2048), mime=True)

            def accept():
                Image.objects.create(image=image, album=album)

            actions = {
                'image/gif': accept,
                'image/jpeg': accept,
                'image/png': accept,
            }

            try:
                actions[filetype]()
            except KeyError:
                raise ValidationError(_('Files with the MIME Content-Type "%s" are not supported. Please only choose images with *.gif, *.jpeg, or *.png file extensions.' % filetype), code='invalid')

    def create_album(self, request):
        # Data collection
        title = request.POST.get('title', '')
        images = request.FILES.getlist('images', [])

        # Validations
        errors = []

        if not title:
            errors.append(ValidationError(_('Please enter a title.'), code='invalid'))

        if not images:
            errors.append(ValidationError(_('Please upload at least one image.'), code='invalid'))

        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            errors.append(ValidationError(_('There was an error retrieving the user\'s ID.'), code='invalid'))

        # Raise errors if any
        if errors:
            raise ValidationError(errors, code='invalid')

        # Album creation
        album = self.create(title=title, created_by=user)

        # Image creation
        self.upload_images(album, images)

        # Return success
        len_images = len(images)
        return {
            'success': 'You have successfully uploaded %d image%s to the album "%s."' % (len_images, '' if len_images == 1 else 's', title),
            'args': [album.slug, album.id],
        }

    def album(self, album_title, album_id):
        from .models import Album, Image

        try:
            album = Album.objects.get(id=album_id)
        except Album.DoesNotExist:
            return (False, {
                'status': 'invalid ID',
                'error': 'The specified album could not be found.',
            })

        if album_title != album.slug:
            return (False, {
                'status': 'invalid slug',
                'args': [album.slug, album_id],
            })

        return (True, {
            'album': album,
            'images': Image.objects.filter(album__id=album_id),
        })

    def update_title(self, request, album_id):
        from .forms import UpdateAlbumTitleForm
        from .models import Album

        form = UpdateAlbumTitleForm(request.POST)

        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to update an album.')

            raise PermissionDenied()

        if form.is_valid():
            # Data collection
            title = form.cleaned_data['title']
            album_id = int(album_id)

            # Validations
            errors = []

            try:
                album = Album.objects.get(id=album_id)
            except Album.DoesNotExist:
                raise ValidationError(_('The specified album could not be found.'), code='not found')

            if album.title == title:
                raise ValidationError(_('Please choose a different title than the existing one.'), code='titles match')

            # Update album
            old_title = album.title
            album.title = title

            # Check permissions
            try:
                if request.user != album.created_by and not request.user.is_superuser:
                    messages.error(request, 'You do not have permission to edit this album.')

                    raise PermissionDenied()
            except User.DoesNotExist:
                messages.error(request, 'You do not have permission to edit this album.')

                raise PermissionDenied()

            album.save()

            return {
                'success': 'The album with the name "%s" has successfully been changed to "%s."' % (old_title, title),
                'args': [album.slug, album_id],
            }

        raise ValidationError(_('The form data entered was not valid.'), code='invalid')

    def add_images(self, request, album_id):
        from .models import Album

        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to update an album.')

            raise PermissionDenied()

        # Data collection
        images = request.FILES.getlist('images', [])
        album_id = int(album_id)

        # Validations
        errors = []

        try:
            album = Album.objects.get(id=album_id)
        except Album.DoesNotExist:
            raise ValidationError(_('The specified album could not be found.'), code='not found')

        # Check permissions
        try:
            if request.user != album.created_by and not request.user.is_superuser:
                messages.error(request, 'You do not have permission to edit this album.')

                raise PermissionDenied()
        except User.DoesNotExist:
            messages.error(request, 'You do not have permission to edit this album.')

            raise PermissionDenied()

        # Image creation
        self.upload_images(album, images)

        len_images = len(images)
        return {
            'success': 'You have successfully added %d image%s to the album "%s."' % (len_images, '' if len_images == 1 else 's', album.title),
            'args': [album.slug, album_id],
        }

class ImageManager(models.Manager):
    pass
