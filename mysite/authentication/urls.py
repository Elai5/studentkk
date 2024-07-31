from django.contrib import admin
from django.urls import path, include
from . import views
from .views import universities_data, send_friend_request, accept_friend_request, decline_friend_request, chat_view  # Ensure these are imported
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('career/', views.career, name="career"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),  # This is your sign-in page
    path('signout', views.signout, name="signout"),
    path('verify_otp', views.verify_otp, name='verify_otp'),
    path('homepage', views.homepage, name="homepage"),
    path('friends/', views.friends, name="friends"),  # This now handles both friends and suggestions
    path('profile', views.profile_view, name='profile_view'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    
    path('universities/', universities_data, name='universities_data'),
    path('friends/send_request/<int:user_id>/', send_friend_request, name='send_friend_request'),
    path('friends/accept_request/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    path('friends/decline_request/<int:request_id>/', decline_friend_request, name='decline_friend_request'),
    path('how_it_works', views.how_it_works, name='how_it_works'),
     path('friends/chat/<int:friend_id>/', chat_view, name='send_message'), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)