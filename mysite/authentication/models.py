from django.contrib.auth.models import AbstractUser
from django.db import models
import random
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    country = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    institution = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    otp_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    password_reset_token = models.CharField(max_length=36, blank=True, null=True)
    token_created_at = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def generate_otp(self):      
        self.otp = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()
        self.save()
        
    def is_otp_valid(self, otp):
        expiry_time = self.otp_created_at + timezone.timedelta(minutes=120)
        return self.otp == otp and timezone.now() < expiry_time

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    country = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    institution = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username

class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='friend_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} (Accepted: {self.accepted})"

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # New field to track if the message has been read

    class Meta:
        indexes = [
            models.Index(fields=['sender', 'recipient']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username}: {self.content[:20]}..."

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.state}, {self.country}"

class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.country}"

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)

class Housing(models.Model):
    country = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    short_description = models.TextField(default="Default description")
    link = models.URLField()
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class Transport(models.Model):
    country = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    short_description = models.TextField(default="Default description")
    link = models.URLField()
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class Culture(models.Model):
    country = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    short_description = models.TextField(default="Default description")
    description = models.TextField()
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title