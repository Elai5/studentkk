from django.contrib import admin
from django.urls import path, include
from . import views
from.views import universities_data


urlpatterns = [
    path('', views.home, name="home"),
    
    # path('index/', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('career/', views.career, name="career"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('universities/', universities_data, name='universities_data'),

]
