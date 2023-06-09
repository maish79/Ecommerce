from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from .views import login, register, logout, ProductList, Profile, ProductCreate, ProductUpdate, ProductDelete

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
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = "account/password_reset.html"), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = "account/password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_resent_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name = 'account/password_reset_complete.html'), name='password_reset_complete'),
    
]