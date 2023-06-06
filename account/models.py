from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    profile_image = models.ImageField(upload_to = 'images', null=True)