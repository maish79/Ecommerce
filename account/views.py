from django.contrib import messages, auth
from django.contrib.auth import models
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from .models import User
from shop.models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


# from .forms import ProfileForm
# from .mixins import FieldsMixin, FormValidMixin, AuthorAccessMixin, SuperUserAccessMixin


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('account:home')
        else:
            messages.error(request, 'Invalid Login')
            return redirect('account:login')
    return render(request, 'account/login.html')
    
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']  
        confirm_password = request.POST['confirm_password'] 
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Someone with this username already exist!')
                return redirect('account:register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'This Email is already exist')
                    return redirect('account:register')
                else:
                    user = User.objects.create_user(first_name = first_name, last_name=last_name, username=username, email=email, password=password)
                    user.save()
                    messages.success(request, 'You Successfully Created account')
                    return redirect('account:login')
        else:
            messages.error(request, 'Passwords are not same')

    return render(request, 'account/register.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You! successfully Logged out')
        return redirect('account:login')
    return redirect('account:login')


class ProductList(LoginRequiredMixin, ListView):
    template_name = 'account/dashboard.html'
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Item.objects.all()
        else:
            return Item.objects.filter(uploader=self.request.user)