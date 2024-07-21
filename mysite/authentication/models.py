from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import datetime
import random

class CustomUser(AbstractUser):
    country = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    institution = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    
    def generate_otp(self):      
        self.otp = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()
        self.save()
        
    def is_otp_valid(self, otp):
        expiry_time = self.otp_created_at + datetime.timedelta(minutes=10)
        return self.otp == otp and timezone.now() < expiry_time