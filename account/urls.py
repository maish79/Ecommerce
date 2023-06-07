from django.urls import path
from django.views.generic.base import TemplateView

from .views import login, register, logout, ProductList, Profile
# ProductCreate, ProductUpdate, ProductDelete

app_name = 'account'
urlpatterns = [
    path('', ProductList.as_view(), name='home'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('profile/', Profile.as_view(), name='profile'),


    
]