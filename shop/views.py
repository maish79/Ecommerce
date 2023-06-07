from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from .forms import CheckOutForm, ReviewForm
from .stripe_payment import stripe_payment
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

def detail(request, slug):
    product = get_object_or_404(Item, slug=slug)
    all_reviews = product.reviews.filter(active=True)
    new_review = None
    if request.method == 'POST':
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.product = product
            new_review.save()
            return HttpResponseRedirect('')
    else:
        review_form = ReviewForm()
    context = {
        'product': product,
        'all_reviews': all_reviews,
        'new_review':new_review,
        'review_form':review_form,
    }
    return render(request, 'detail.html', context)

def category(request, slug):
    context = {
        "category": get_object_or_404(Category, slug=slug),
    }

    return render(request, 'category.html', context)