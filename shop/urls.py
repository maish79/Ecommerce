from django.urls import path
from .views import  *

app_name = 'shop'
urlpatterns = [
    path('', Home, name = 'home'),
    path('product/<slug:slug>/', detail, name = 'product'),
    path('category/<slug:slug>/', category, name = 'category'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('checkout/',CheckOutView.as_view(), name = 'checkout'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('increase-quantity/<slug>/', increase_quantity, name='increase-quantity'),
    path('decrease-quantity/<slug>/', decrease_quantity, name='decrease-quantity'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('delete-from-cart/<int:order_item_id>/', delete_from_cart, name='delete_from_cart'),

]

