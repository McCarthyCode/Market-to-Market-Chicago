from django.db import models
from django.contrib.auth.models import User
from users import managers

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    objects = managers.ProfileManager()

class Author(Profile):
    profile_pic = models.ImageField(upload_to='media/img/')
    bio = models.CharField(max_length=500)
