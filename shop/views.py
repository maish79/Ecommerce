from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import CheckOutForm, ReviewForm
from .models import *
from .stripe_payment import stripe_payment
import stripe

from django.views.decorators.http import require_POST

from django.db.models import Q
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



class OrderSummaryView(LoginRequiredMixin, View):
    '''
    Renders order-summary page
    '''
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            return render(self.request, 'order-summary.html', {'object': order})
        except ObjectDoesNotExist:
            return redirect('/')

from django.views.decorators.http import require_POST

@require_POST
def delete_from_cart(request, order_item_id):
    order_item = OrderItem.objects.get(id=order_item_id)
    order_item.delete()
    messages.success(request, "Item has been removed from your cart.")
    return redirect('shop:home')



@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Find the OrderItem and update the quantity
        order_item = order.items.filter(item__slug=slug)
        if order_item.exists():
            quant = order_item[0].quantity
            messages.info(request, "This item is already in your cart.")
        else:
            order_item = OrderItem.objects.create(item=item)
            order.items.add(order_item)
            messages.info(request, "This item has been added to your cart")
    else:
        # Create new order
        ordered_date = timezone.now()
        order_item = OrderItem.objects.create(item=item)
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item has been added to your cart")
    return redirect('shop:product', slug=slug)


@require_POST
def delete_from_cart(request, order_item_id):
    order_item = OrderItem.objects.get(id=order_item_id)
    order_item.delete()
    messages.success(request, "Item has been removed from your cart.")
    return redirect('shop:home')
