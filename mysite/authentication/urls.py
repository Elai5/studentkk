from django.contrib import admin
from django.urls import path, include
from . import views
from.views import universities_data
from .views import friend_suggestions, send_friend_request


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('career/', views.career, name="career"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('verify_otp', views.verify_otp, name='verify_otp'),
    path('homepage', views.homepage, name="homepage"),
    path('friends', views.friends, name="friends"),
    path('universities/', universities_data, name='universities_data'),
    path('friends/suggestions/', friend_suggestions, name='friend_suggestions'),
    path('friends/send_request/<int:user_id>/', send_friend_request, name='send_friend_request'),

]
