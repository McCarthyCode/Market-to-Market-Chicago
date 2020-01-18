from django.db import models

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
        return (True, 'You have successfully uploaded %d image%s to the album \'%s\'.' % (len_images, '' if len_images == 1 else 's', title))


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
