from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .models import *
# Create your views here.


def Home(request):
    products = Item.objects.all()
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories
    }

    return render(request, 'home.html', context)

   

def category(request, slug):
    context = {
        "category": get_object_or_404(Category, slug=slug),
    }

    return render(request, 'category.html', context)