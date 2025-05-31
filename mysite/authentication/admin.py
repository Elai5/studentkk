from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import CustomUser, Housing, Transport, Culture
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display =  ('username', 'first_name', 'last_name', 'email', 
        'country', 'location', 'institution', 'city', 
        'state', 'zip_code', 'profile_picture' )

admin.site.register(CustomUser, CustomUserAdmin)

# Register Housing model with default admin
@admin.register(Housing)
class HousingAdmin(admin.ModelAdmin):
    list_display = ('country', 'title', 'short_description', 'link', 'image')  

@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ('country', 'title', 'short_description', 'link', 'image')  

@admin.register(Culture)
class CultureAdmin(admin.ModelAdmin):
    list_display = ('country', 'title', 'short_description', 'description', 'image') 

