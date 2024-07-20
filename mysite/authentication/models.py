from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    country = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    institution = models.CharField(max_length=100, null=True, blank=True)

# Update your settings to use the custom user model
# settings.py
