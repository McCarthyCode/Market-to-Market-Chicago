from django.db import models

class AlbumManager(models.Manager):
    def create_album(self):
        pass

class ImageManager(models.Manager):
    def create_image(self):
        pass
