from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from .views import login, register, logout, ProductList, Profile, ProductCreate, ProductUpdate, ProductDelete
from django.urls.base import reverse_lazy
app_name = 'account'
urlpatterns = [
    path('', ProductList.as_view(), name='home'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('profile/', Profile.as_view(), name='profile'),
    path('product/create/', ProductCreate.as_view(), name='product-create'),
    path('product/update/<int:pk>', ProductUpdate.as_view(), name='product-update'),
    path('product/delete/<int:pk>', ProductDelete.as_view(), name='product-delete'),
    
]