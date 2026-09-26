from django.urls import path
from .views import *


urlpatterns = [

    path('home/',home,name='home'),
    path('login/',user_login,name='login'),
    path('signin/',register_user,name='signin'),
    path('apply/<int:id>/',apply_course,name='apply'),
    path('logout/',logout_user,name='logout'),
    path('success/',success_page,name='success'),

]