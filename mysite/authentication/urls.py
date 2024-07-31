from django.contrib import admin
from django.urls import path, include
from . import views
from.views import universities_data
from .views import friend_suggestions, send_friend_request
from django.conf import settings
from django.conf.urls.static import static
from .views import profile_view


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('career/', views.career, name="career"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('verify_otp', views.verify_otp, name='verify_otp'),
    path('homepage', views.homepage, name="homepage"),
    path('friends/', views.friends, name="friends"),
    path('profile', profile_view, name='profile_view'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    
    path('universities/', universities_data, name='universities_data'),
    path('friends/suggestions', friend_suggestions, name='friend_suggestions'),
    path('friends/send_request/<int:user_id>/', send_friend_request, name='send_friend_request'),
    path('friend-suggestions', friend_suggestions, name='friend_suggestions'),
    path('send-friend-request/<int:user_id>/', send_friend_request, name='send_friend_request'),
    path('friend-suggestions/', friend_suggestions, name='friend_suggestions'),
    path('send-friend-request/<int:user_id>/', send_friend_request, name='send_friend_request'),
    path('how_it_works', views.how_it_works, name='how_it_works'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
