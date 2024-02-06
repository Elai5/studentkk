from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    # Additional fields
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)

    def __str__(self):
        return self.username
