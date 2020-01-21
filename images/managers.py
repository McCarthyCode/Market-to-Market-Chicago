from django.db import models
from django.shortcuts import reverse

class AlbumManager(models.Manager):
    def create_album(self, request):
        from .models import Image

        # Data collection
        title = request.POST.get('title', '')
        images = request.FILES.getlist('images', [])

        # Validations
        errors = []

        if not title:
            errors.append('Please enter a title.')

        if not images:
            errors.append('Please upload at least one image.')

        # Return failure
        if errors:
            return (False, errors)

        # Album creation
        album = self.create(title=title)

        # Image creation
        for image in images:
            Image.objects.create_image(image=image, album=album)

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

        # left_column = center_column = right_column = []

        # def left(image):
        #     left_column.append(image)

        # def center(image):
        #     center_column.append(image)

        # def right(image):
        #     right_column.append(image)

        # actions = {
        #     0: left,
        #     1: center,
        #     2: right,
        # }

        # i = 0
        # for image in Image.objects.filter(album__id=album_id):
        #     actions[i % 3](image)
        #     i += 1

        return (True, {
            'album': album,
            'images': Image.objects.filter(album__id=album_id),
        })


class ImageManager(models.Manager):
    def create_image(self, **kwargs):
        # Validations (raise error)
        if 'image' not in kwargs and 'album' not in kwargs:
            raise TypeError("create_image() missing 2 required keyword arguments 'image' and 'album'")
        elif 'image' not in kwargs:
            raise TypeError("create_image() missing 1 required keyword argument 'image'")
        elif 'album' not in kwargs:
            raise TypeError("create_image() missing 1 required keyword argument 'album'")

        # Return image object
        return self.create(image=kwargs['image'], album=kwargs['album'])
