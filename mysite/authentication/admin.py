from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'country', 'location', 'institution')  # Add other fields as needed

admin.site.register(CustomUser, CustomUserAdmin)
