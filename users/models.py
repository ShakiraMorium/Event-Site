from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
   
    profile_image = models.ImageField(upload_to='profile_img/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
