from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _

class AlbumManager(models.Manager):
    def create_album(self, request):
        from .models import Image

        # Data collection
        title = request.POST.get('title', '')
        images = request.FILES.getlist('images', [])
        user_id = int(request.POST.get('user-id', '0'))

        # Validations
        errors = []

        if not title:
            errors.append('Please enter a title.')

        if not images:
            errors.append('Please upload at least one image.')

        if not user_id:
            errors.append('There was an error retrieving the user\'s ID.')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            errors.append('A user with the specified ID could not be found.')

        # Return failure
        if errors:
            return (False, errors)

        # Album creation
        album = self.create(title=title, created_by=user)

        # Image creation
        for image in images:
            Image.objects.create(image=image, album=album)

        # Return success
        len_images = len(images)
        return (True,
            'You have successfully uploaded %d image%s to the album <a href="%s">%s</a>.' %
            (len_images,
            '' if len_images == 1 else 's',
            reverse('images:album', args=[album.slug, album.id]),
            title)
        )

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

            if album_id < 1:
                raise ValidationError(_('Invalid album ID.'), code='invalid')

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
                'success': 'The album with the name \'%s\' has successfully been changed to \'%s\'.' % (old_title, title),
                'args': [album.slug, album_id],
            }

        raise ValidationError()

class ImageManager(models.Manager):
    pass
