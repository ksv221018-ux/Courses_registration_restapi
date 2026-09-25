from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('home/',get_course),
    path('login-page/',user_login),
    path('signin-page/',register_user),
    path('apply/<int:id>/', apply_course),
    path('success-page/', success_page),
    path(
        'apply/<int:id>/',
        apply_course,
        name='apply_course'
    ),
]