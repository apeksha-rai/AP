from django.core.mail import EmailMessage
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import render_to_string
from django.views.generic.base import View
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from .models import *


class BaseView(View):
        views = dict()
        views['sliders'] = Slider.objects.filter(status='active')
        views['brands'] = Brand.objects.filter(status='active')
        views['count'] = []
        for i in views['brands']:
            count_brand = Item.objects.filter(brand=i.id).count()
            g = {'name': i.name, 'count': count_brand}
            views['count'].append(g)
        views['items'] = Item.objects.filter(status='active')
        views['item_count'] = Item.objects.count()
        views['count_cat'] = Category.objects.filter(status='active')
        views['cat_count'] = []
        for i in views['count_cat']:
            count_aria = Item.objects.filter(category=i.id).count()
            h = {'name': i.title, 'image': i.image, 'count': count_aria}
            views['cat_count'].append(h)
        # simply counts all item entries in Item model/database
        views['item_count'] = Item.objects.count()


class HomeView(BaseView):
    def get(self,request):
        self.views['categories'] = Category.objects.filter(status = 'active')
        self.views['ads'] = Ad.objects.filter(status='active')
        self.views['hots'] = Item.objects.filter(label='hot')
        self.views['news'] = Item.objects.filter(label='new')
        self.views['most_viewed'] = Item.objects.filter(label='most_viewed')
        self.views['defaults'] = Item.objects.filter(label='')
        return render(request, 'index.html', self.views)


class ItemDetailView(BaseView):
    def get(self, request, slug):
        self.views['item_detail'] = Item.objects.filter(slug=slug)
        item_ids = Item.objects.get(slug=slug).category_id
        self.views['item_cats'] = Item.objects.filter(category=item_ids)
        self.views['reviews'] = Review.objects.filter(slug=slug, status='active')
        return render(request, 'product-detail.html', self.views)


class ItemListView(BaseView):
    def get(self, request, slug):
        cat_ids = Category.objects.get(slug=slug).id
        self.views['cat_items'] = Item.objects.filter(category=cat_ids)
        return render(request, 'product-list.html', self.views)


class SearchView(BaseView):
    def get(self, request):
        # query = request.GET.get('search', None)
        if request.method == 'GET':
            query = request.GET['search']
            self.views['search_product'] = Item.objects.filter(item_name__icontains=query)
            return render(request, 'search.html', self.views)
        return render(request, 'search.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        data = Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        # check entered user data is correct or not by python validators
        # saves form data to DB
        if len(name) < 3 or len(subject) < 5 or len(message) < 5:
            messages.error(request, 'Please re-submit the message!')
        else:
            send_email = EmailMessage(
                'contact from your website',
                f'Hello admin, {name} is trying to contact you. His email is {email}. He want to talk about {subject}.'
                f'His message is {message}.',
                settings.EMAIL_HOST_USER,
                ['rowjune1@gmail.com'],
                [request.user.email],
            )
            send_email.fail_silently = False
            send_email.send()
            data.save()
            return redirect('/', kwargs={'messages': messages.success(request,
                                                                      '✔ Contact is saved also check your mail!')})
    return render(request, 'contact.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        fname = request.POST['fname']
        lname = request.POST['lname']

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, '❌ This username is already taken!')
                return redirect('home:account')
            elif User.objects.filter(email=email).exists():
                messages.error(request, '❌ This email is already taken!')
                return redirect('home:account')
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=fname,
                    last_name=lname
                )
                user.save()
                messages.success(request, '✔️You are registered! Continue to login!')
                return redirect('/accounts/login', messages)
        else:
            messages.error(request, '❌ These passwords do not match!')
            return redirect('home:account')
    return render(request, 'signup.html')


def review_item(request):
    if request.method == 'POST':
        rating = request.POST['rating']
        review = request.POST['review']
        username = request.user.username
        email = request.user.email
        slug = request.POST['slug']

        user_review = Review.objects.create(
            rating=rating,
            username=username,
            review=review,
            email=email,
            slug=slug
        )
        user_review.save()
        messages.success(request, '✔️Your review is successfully submitted!')
        return redirect(f'/products/{slug}')


def cart(request, slug):
    price = Item.objects.get(slug=slug).price
    discounted_price = Item.objects.get(slug=slug).discounted_price
    user = request.user.username
    net_total = 0
    shipping_cost = 1000
    if Cart.objects.filter(slug=slug).exists():
        quantity = Cart.objects.get(username=user, slug=slug, checkout=False).quantity
        qty = quantity + 1
        if discounted_price > 0:
            actual_total = discounted_price * qty
        else:
            actual_total = price * qty
        Cart.objects.filter(username=user, slug=slug, checkout=False).update(
            quantity=qty, total=actual_total)

        total = Cart.objects.filter(username=user, checkout=False, status='active')

        for i in total[:]:
            net_total += i.total
        grand_total = net_total + shipping_cost

        CartTotal.objects.filter(username=user, checkout=False).update(
            net_total=net_total, shipping_cost=shipping_cost, grand_total=grand_total)
        return redirect('home:my_cart')

    else:
        if discounted_price > 0:
            actual_total = discounted_price * 1
        else:
            actual_total = price * 1
        data = Cart.objects.create(
            username=user,
            slug=slug,
            quantity=1,
            total=actual_total,
            items=Item.objects.filter(slug=slug)[0]

        )
        Cart.objects.filter(username=user, slug=slug, checkout=False).update(checkout=False, total=actual_total)
        total = Cart.objects.filter(username=user, checkout=False, status='active')

        for i in total[:]:
            net_total += i.total
        grand_total = net_total + shipping_cost
        data1 = CartTotal.objects.create(
            username=user,
            slug=slug,
            net_total=net_total,
            shipping_cost=shipping_cost,
            grand_total=grand_total,
            cart=Cart.objects.filter(slug=slug)[0]
        )
        data.save()
        data1.save()
        messages.success(request, f'✔️The item "{slug}" is added in cart!')
        CartTotal.objects.filter(username=user, checkout=False).update(net_total=net_total, shipping_cost=shipping_cost, grand_total=grand_total)
        return redirect('home:my_cart')


class CartView(BaseView):
    def get(self, request):
        user = request.user.username
        net_total = 0
        shipping_cost = 1000
        grand_total = 0
        self.views['cart_product'] = Cart.objects.filter(username=user, checkout=False, status='active')
        tots = CartTotal.objects.filter(username=user, checkout=False)
        for i in tots[:]:
            net_total = i.net_total
            shipping_cost = i.shipping_cost
            grand_total = i.grand_total
        self.views['cart_total'] = [{'net_total': net_total, 'shipping_cost': shipping_cost, 'grand_total': grand_total}]
        self.views['cart_count'] = Cart.objects.filter(username=user, status='active', checkout=False).count()
        return render(request, 'cart.html', self.views)


def delete_cart(request, slug):
    if Cart.objects.filter(slug=slug).exists():
        user = request.user.username
        net_total = 0
        t = 0
        shipping_cost = 1000
        grand_total = 0
        b = Cart.objects.filter(username=user, slug=slug, checkout=False, status='active')
        tots = CartTotal.objects.filter(username=user, checkout=False)
        for j in b[:]:
            t = j.total
        for i in tots[:]:
            net_total = i.net_total
            shipping_cost = i.shipping_cost
            grand_total = i.grand_total
        net_total = net_total - t
        grand_total = net_total + shipping_cost
        Cart.objects.filter(username=user, slug=slug, checkout=False).delete()
        CartTotal.objects.filter(username=user, checkout=False).update(net_total=net_total, grand_total=grand_total,
                                                                       shipping_cost=shipping_cost)

        if Cart.objects.count() == 0:
            messages.info(request, 'You have 0 items in the Cart!')
            net_total = net_total
            grand_total = grand_total
            shipping_cost = shipping_cost
            CartTotal.objects.filter(username=user, checkout=False).update(net_total=net_total, grand_total=grand_total,
                                                                           shipping_cost=shipping_cost)
            return redirect('home:my_cart')

    return redirect('home:my_cart')


def delete_single_cart(request, slug):
    if Cart.objects.filter(slug=slug).exists():
        net_total = 0
        shipping_cost = 1000
        user = request.user.username
        price = Item.objects.get(slug=slug).price
        discounted_price = Item.objects.get(slug=slug).discounted_price
        quantity = Cart.objects.get(username=user, slug=slug, checkout=False).quantity
        if quantity > 1:
            qty = quantity - 1
            if discounted_price == 0:
                actual_total = price*qty
            else:
                actual_total = discounted_price*qty
            Cart.objects.filter(username=user, slug=slug, checkout=False).update(
                quantity=qty, checkout=False, total=actual_total)
        total = Cart.objects.filter(username=user, checkout=False, status='active')

        for i in total[0:]:
            net_total += i.total
        grand_total = net_total + shipping_cost
        CartTotal.objects.filter(username=user, checkout=False).update(
            net_total=net_total, shipping_cost=shipping_cost, grand_total=grand_total)
    return redirect('home:my_cart')


class CheckoutView(BaseView):
    def post(self, request):
        template = render_to_string('email/email.html', {'name': request.user.username})
        if request.method == 'POST':
            username = request.user.username
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            shipping_add = request.POST['shipping_add']
            mobile_no = request.POST['mobile_no']
            zip_code = request.POST['zip_code']
            data = CheckoutCart.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                shipping_add=shipping_add,
                mobile_no=mobile_no,
                zip_code=zip_code,
            )
            data.save()
            send_email = EmailMessage(
                'Checkout completed',
                template,
                settings.EMAIL_HOST_USER,
                ['apeksharai3944@gmail.com'],
                [email],
            )
            send_email.fail_silently = False
            send_email.send()
            Cart.objects.all().delete()
            CartTotal.objects.all().delete()
            CheckoutCart.objects.all().delete()
            messages.success(request, '✔ Checkout completed! check mail!')
            return redirect("/")

    def get(self, request):
        user = request.user.username
        net_total = 0
        shipping_cost = 1000
        grand_total = 0
        self.views['cart_product'] = Cart.objects.filter(username=user, checkout=False, status='active')
        tots = CartTotal.objects.filter(username=user, checkout=False)
        for i in tots[:]:
            net_total = i.net_total
            shipping_cost = i.shipping_cost
            grand_total = i.grand_total
        self.views['cart_total'] = [
            {'net_total': net_total, 'shipping_cost': shipping_cost, 'grand_total': grand_total}]
        return render(request, 'checkout.html', self.views)


# ------------------------API--------------------------
from rest_framework import viewsets
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from home.serializers import ItemSerializers
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter


# managed from router
# ViewSets define the view behavior.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializers


# needs a url to be managed
class ProductListView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializers
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filter_fields = ['id', 'category', 'label', 'brand']
    ordering_fields = ['id', 'price', 'name']
    search_fields = ['item_name', 'desc']