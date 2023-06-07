from django.urls import path
from django.views.generic.base import TemplateView


from .views import login, register, logout
from django.contrib.auth import views as auth_views

app_name = 'account'
urlpatterns = [

    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),


    
]