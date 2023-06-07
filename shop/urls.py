from django.urls import path
from .views import  *

app_name = 'shop'
urlpatterns = [
    path('', Home, name = 'home'),
    path('product/<slug:slug>/', detail, name = 'product'),
    path('category/<slug:slug>/', category, name = 'category'),

]