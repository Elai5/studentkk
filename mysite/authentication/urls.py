from django.contrib import admin
from django.urls import path, include
from . import views
from .views import (
    universities_data,
    send_friend_request,
    accept_friend_request,
    decline_friend_request,
    chat_list_view,
    chat_view,
    password_reset_request,
    password_reset_confirm,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('verify_otp', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),  # Updated path for resend OTP
    path('homepage', views.homepage, name="homepage"),
    path('friends/', views.friends, name="friends"),
    path('profile', views.profile_view, name='profile_view'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('universities/', universities_data, name='universities_data'),
    path('friends/send_request/<int:user_id>/', send_friend_request, name='send_friend_request'),
    path('friends/accept_request/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    path('friends/decline_request/<int:request_id>/', decline_friend_request, name='decline_friend_request'),
    
    # Chat URLs
    path('chat', chat_list_view, name='chat_list'),  # URL for chat list
    path('chat/<int:friend_id>/', chat_view, name='chat_with_friend'),  # URL for chatting with a specific friend

    path('how_it_works', views.how_it_works, name='how_it_works'),
    path('testimonials', views.testimonials, name='testimonials'),
    path('password-reset/', password_reset_request, name='password_reset_request'),
    path('password-reset-confirm/<str:token>/', password_reset_confirm, name='password_reset_confirm'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)