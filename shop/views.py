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


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        order_item = order.items.filter(item__slug=slug)
        # Delete item from the cart
        if order_item.exists():
            order.items.remove(order_item[0])
            messages.info(request, "Item successfully removed from your cart")
        else:
            messages.info(request, "No such item in your cart")
    else:
        messages.info(request, "No such item in your cart")

    return redirect('shop:product', slug=slug)



@login_required
def decrease_quantity(request, slug):
    '''
    Decrease slug-item from the cart by one unit.
    :param request: POST request
    :param slug: Unique slug of the item
    :return: Rendered page
    '''
    #Get the Item and its Order
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        order_item = order.items.filter(item__slug=slug)
        if order_item.exists():
            quant = order_item[0].quantity
            if (quant > 1):
                #Decrease amount by one unit
                order_item.update(quantity=quant - 1)
        else:
            messages.info(request, "No such item in your cart")

    else:
        messages.info(request, "No such item in your cart")

    return redirect('shop:order-summary')

@login_required
def increase_quantity(request, slug):
    '''
    Increase slug-item from the cart by one unit.
    :param request: POST request
    :param slug: Unique slug of the itenm
    :return: Rendered page
    '''

    #Get the Item and its Order
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        order_item = order.items.filter(item__slug=slug)
        if order_item.exists():
            quant = order_item[0].quantity
            # Increase quanity by one unit
            order_item.update(quantity=quant + 1)
        else:
            messages.info(request, "No such item in your cart")

    else:
        messages.info(request, "No such item in your cart")

    return redirect('shop:order-summary')


def search(request):
    products = Item.objects.all()

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = products.filter(Q(description__icontains=keyword)|Q(title__icontains=keyword))
    context = {
        'products': products,
    }
    return render(request, 'search.html', context)


class CheckOutView( LoginRequiredMixin,  View):
    '''
    Checkout page
    1. Save shipping address and related information
    '''
    def get(self, *args, **kwargs):
        form = CheckOutForm()
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {'form': form, 'order':order}
            return render(self.request, 'checkout-page.html', context)
        except ObjectDoesNotExist:
            return redirect('/')


    def post(self, *args, **kwargs):
        form = CheckOutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user= self.request.user, ordered = False)

            if form.is_valid():
                # Get the shipping information and save them into the database.
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                same_shipping_address = form.cleaned_data.get('same_shipping_address')
                save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billingAddress = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip,
                )
                billingAddress.save()
                # Connect address with order (Foreign Key)
                order.billing_address = billingAddress
                order.save()
                return redirect('shop:payment', payment_option= payment_option)
            return render(self.request, 'checkout-page.html', {'form':form})

        except ObjectDoesNotExist:
            messages.warning(self.request, "You don't have any active order")
            return redirect('shop:order-summary')


class PaymentView(LoginRequiredMixin, View):
    '''
    Handle Stripe payment (Stripe API)
    '''
    def get (self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'STRIPE_PUBLIC_KEY': settings.STRIPE_SECRET_KEY,
            'order': order
        }
        return render (self.request, 'payment.html', context)

    def post(self,*args, **kwargs):
        # Create Stripe payment
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        chargeID = stripe_payment(settings.STRIPE_SECRET_KEY,token, order.get_total(), str(order.id))
        if (chargeID is not None):
            order.ordered = True

            # Save the payment
            payment = Payment()
            payment.stripe_charge_id = chargeID
            payment.user = self.request.user
            payment.price = order.get_total() * 100
            payment.save()
            order.payment = payment
            order.save()
            return redirect('/')
        else:
            messages.error(self.request, "Something went wrong with Stripe. Please try again later")
            return redirect ('shop:payment', payment_option= 'S')
