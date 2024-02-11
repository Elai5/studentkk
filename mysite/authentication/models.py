from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    country = models.CharField(max_length=50)
    institution = models.CharField(max_length=100)
    location = models.CharField(max_length=20)
    # Add other custom fields as needed

    def __str__(self):
        return self.username
