from account.models import User
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField




class Category(models.Model):
    title = models.CharField(max_length=202)
    slug = models.SlugField(max_length=100, unique=True)
    
    def __str__(self):
        return self.title

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class Item(models.Model):
    uploader = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='products')
    title = models.CharField(max_length= 100)
    slug = models.SlugField(unique= True)
    price = models.FloatField()
    image = models.ImageField(upload_to='images')
    description = models.TextField()
    category = models.ManyToManyField(Category, related_name='products')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ('shop:product', kwargs = {'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse ('shop:add-to-cart', kwargs = {'slug': self.slug})

    def get_price(self):         
        return self.price



class Review(models.Model):
    product = models.ForeignKey(Item, on_delete=models.CASCADE,related_name='reviews')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    description = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_time']

    def __str__(self):
        return 'Review {} by {}'.format(self.description, self.name)



class OrderItem(models.Model):
    item = models.ForeignKey (Item , on_delete= models.CASCADE)
    quantity = models.IntegerField (default= 1)


    def __str__(self):
        return str(self.item.title) + str(self.quantity)

    def get_total_price (self):
        return self.quantity * self.item.price

    def get_amount_saved(self):     
        return 0



class Order(models.Model):
    user = models.ForeignKey (User, on_delete= models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date  = models.DateTimeField()
    ordered = models.BooleanField(default= False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=  models.SET_NULL, blank= True,
                                        null= True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True,
                                        null=True)

    def __str__(self):
        return self.user.username

    def get_total (self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_price()
        return total

class BillingAddress(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)


    def __str__(self):
        return self.user.username


class Payment(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    stripe_charge_id = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
