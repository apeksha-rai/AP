from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
STATUS = (('active','active'),('','defult'))
PRODUCT_LABEL = (('new', 'new'), ('hot', 'hot'), ('most_viewed', 'most_viewed'), ('', 'default'))
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    image = models.CharField(max_length=200)
    status = models.CharField(default='active', choices=STATUS, max_length=100)

    def __str__(self):
        return self.title

    def get_cat_url(self):
        return reverse('home:category', kwargs={'slug': self.slug})


class Slider(models.Model):
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='media/')
    description = models.TextField(blank=True)
    status = models.CharField(choices=STATUS, max_length=200)

    def __str__(self):
        return self.name


class Ad(models.Model):
    title = models.CharField(max_length=200)
    desc = models.TextField(blank=True)
    image = models.ImageField(upload_to='media/')
    status = models.CharField(default='active', choices=STATUS, max_length=100)
    rank = models.IntegerField(unique=True)

    def __str__(self):
        return self.title


class Brand(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/')
    status = models.CharField(default='active', choices=STATUS, max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    item_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/')
    slug = models.CharField(max_length=200, unique=True)
    price = models.IntegerField()
    discounted_price = models.IntegerField()
    discount = models.IntegerField()
    status = models.CharField(default='active', choices=STATUS, max_length=100)
    label = models.CharField(choices=PRODUCT_LABEL, max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    desc = models.TextField(blank=True)
    specification = models.TextField(blank=True)

    def __str__(self):
        return self.item_name

    def get_item_url(self):
        return reverse('home:products', kwargs={'slug': self.slug})

    def get_cart_url(self):
        return reverse('home:cart', kwargs={'slug': self.slug})
# when Category is deleted, Item/s also gets deleted


class Contact(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(max_length=200, blank=True)
    subject = models.TextField(blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name


class Review(models.Model):
    username = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    review = models.TextField(blank=True)
    rating = models.IntegerField()
    date_posted = models.DateTimeField(default=timezone.now)
    status = models.CharField(default='active', choices=STATUS, max_length=200)
    slug = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.username


class SiteReview(models.Model):
    name = models.CharField(max_length=200)
    profession = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/')
    status = models.CharField(default='active', choices=STATUS, max_length=100)
    review = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    username = models.CharField(max_length = 300)
    slug = models.CharField(max_length = 300)
    items = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)
    total = models.IntegerField(default = 0)
    status = models.CharField(max_length=50, choices=STATUS, default='active', null=True)
    checkout = models.BooleanField(default = False)

    def __str__(self):
        return self.username


class CartTotal(models.Model):
    username = models.CharField(max_length=200, default=None)
    net_total = models.IntegerField(default=0)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, default=None)
    slug = models.CharField(max_length=100, unique=True, default=None)
    shipping_cost = models.IntegerField(default=0)
    grand_total = models.IntegerField(default=0)
    checkout = models.BooleanField(default=False)
    date_checked = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username


class CheckoutCart(models.Model):
    first_name = models.CharField(max_length=200, default=None)
    last_name = models.CharField(max_length=200, default=None)
    username = models.CharField(max_length=200, null=True)
    email = models.EmailField()
    shipping_add = models.CharField(max_length=200)
    mobile_no = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    zip_code = models.CharField(max_length=20, default=None)

    def __str__(self):
        return self.first_name
