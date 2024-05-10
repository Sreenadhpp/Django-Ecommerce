from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.db.models import Q
from django.conf import settings
from django.http import JsonResponse

import razorpay

from .models import Product, Cart, Payment, Orderplaced, Wishlist
from users.models import Customer

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def home(request):
    products = Product.objects.all()

    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        user = request.user
        totalitem = len(Cart.objects.filter(user=user))
        wishitem = len(Wishlist.objects.filter(user=user))

    return render(request, 'app/home.html', locals())


def about(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        user = request.user
        totalitem = len(Cart.objects.filter(user=user))
        wishitem = len(Wishlist.objects.filter(user=user))

    return render(request, 'app/about.html', locals())


def contact(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        user = request.user
        totalitem = len(Cart.objects.filter(user=user))
        wishitem = len(Wishlist.objects.filter(user=user))

    return render(request, 'app/contact.html', locals())


class CategoryView(View):
    def get(self, request,catgry):
        catgry_products = Product.objects.filter(category=catgry)
        prodt_titles = Product.objects.filter(category=catgry).values('title')

        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            user = request.user
            totalitem = len(Cart.objects.filter(user=user))
            wishitem = len(Wishlist.objects.filter(user=user))

        return render(request, "app/category.html", locals())

class CategoryTitle(LoginRequiredMixin, View):
    def get(self, request, title):
        
        catgry_products = Product.objects.filter(title=title)
        prodt_titles = Product.objects.filter(category=catgry_products[0].category)    # may be use .values('title')
        
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            user = request.user
            totalitem = len(Cart.objects.filter(user=user))
            wishitem = len(Wishlist.objects.filter(user=user))

        return render(request, 'app/category.html', locals())
        
    
class ProductDetail(View):
    def get(self,request,pk):
        product = get_object_or_404(Product, id=pk)

        totalitem = 0
        wishitem = 0
        if self.request.user.is_authenticated:
            user = self.request.user
            wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=user))
            wishitem = len(Wishlist.objects.filter(user=user))
            totalitem = len(Cart.objects.filter(user=user))
        return render(request, 'app/product_detail.html', locals())
    

@login_required
def AddToCart(request):
    if request.user.is_authenticated:
        user = request.user
        product_id = request.GET.get('prod_id')
        
        if Cart.objects.filter(Q(products=product_id) & Q(user=user)).exists():

            cart = Cart.objects.get(Q(products=product_id) & Q(user=user))
            cart.quantity += 1
            cart.save()
        
        else:
            product = get_object_or_404(Product, id = product_id)
            Cart(user=user, products=product).save()
        return redirect('showcart')
    

@login_required
def ShowCart(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        user = request.user
        totalitem = len(Cart.objects.filter(user=user))
        wishitem = len(Wishlist.objects.filter(user=user))

        cart = Cart.objects.filter(user=user)

        amount = 0
        for item in cart:
            one_pro_value = item.products.discounted_price * item.quantity
            amount = amount + one_pro_value
        totalamount = amount + 40    
        
    return render(request, 'app/showcart.html', locals())


@method_decorator(login_required, name='dispatch')
class checkout(View):
    def get(self, request): 
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            user = request.user
            totalitem = len(Cart.objects.filter(user=user))
            wishitem = len(Wishlist.objects.filter(user=user))

        add = Customer.objects.filter(user = self.request.user)
        print(add)
        cart_items  = Cart.objects.filter(user=self.request.user)
        
        cust_id = request.GET.get('cust_id')
        print(cust_id)

        famount = 0
        for item in cart_items:
            value = item.products.discounted_price * item.quantity
            famount = famount + value
        totalamount = famount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth = (settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

        data = { "amount": razoramount, "currency": "INR", "receipt": "order_rcptid_11" }
        payment_response = client.order.create(data=data)
        print(payment_response)

        #{'id': 'order_M8qh3l1aVlYMmT', 'entity': 'order', 'amount': 32000, 'amount_paid': 0, 'amount_due': 32000, 'currency': 'INR', 
        # 'receipt': 'order_rcptid_11', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1688282594}

        order_id = payment_response['id']
        order_status = payment_response['status']

        if order_status == 'created':
            payment = Payment(
                user = self.request.user,
                amount = totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status
            )
            payment.save()
            print(payment.razorpay_order_id)
            print(payment.razorpay_payment_id)
            print(payment.paid)

        return render(request, 'app/checkout.html', locals())


@login_required
def paymentDone(request):
    if request.user.is_authenticated:
        user = request.user

        order_id = request.GET.get('order_id')
        payment_id = request.GET.get('payment_id')
        cust_id = request.GET.get('cust_id')
        print(order_id )
        print(payment_id)
        print(cust_id)

        # return redirect("orders")
        customer = Customer.objects.get(id = cust_id)

        # To update payment status and payment id
        payment = Payment.objects.get(razorpay_order_id = order_id)
        payment.paid = True
        payment.razorpay_payment_id = payment_id
        payment.save()

        # To save order details
        cart = Cart.objects.filter(user=user)
        for c in cart : 
            Orderplaced(user=user, customer=customer, product=c.products, quantity = c.quantity, payment = payment ).save()
            c.delete()
    return redirect("orders")


@login_required
def orders(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        user = request.user
        totalitem = len(Cart.objects.filter(user=user))
        wishitem = len(Wishlist.objects.filter(user=user))

        order_placed = Orderplaced.objects.filter(user=user)

    return render(request, 'app/orders.html', locals())


@login_required
def PlusCart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        user = request.user
        c= Cart.objects.get(Q(products = prod_id) & Q(user = user))
        c.quantity += 1
        c.save()

        cart = Cart.objects.filter(user=user)
        amount = 0
        for item in cart:
            one_pro_value = item.products.discounted_price * item.quantity
            amount = amount + one_pro_value
        totalamount = amount + 40

        data = {
            'quantity' : c.quantity, 'amount' : amount, 'totalamount' : totalamount 
        }

        return JsonResponse(data)
    

@login_required
def minusCart(request):
    if request.method == "GET" and request.user.is_authenticated:
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(products = prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()

        if c.quantity ==0:
            c.delete()

        cart = Cart.objects.filter(user = request.user)
        amount = 0
        for item in cart:
            one_pro_value = item.products.discounted_price * item.quantity
            amount += one_pro_value
        totalamount = amount + 40
        print(prod_id)
        data = {
                'quantity' : c.quantity, 'amount' : amount, 'totalamount' : totalamount
        }
        return JsonResponse(data)


@login_required
def removeCart(request):
    if request.method == "GET" and request.user.is_authenticated:
        user = request.user
        
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(products = prod_id) & Q(user=user))
        c.delete()
        
        cart = Cart.objects.filter(user = user)
        
        amount = 0
        for item in cart:
            one_pro_value = item.quantity * item.products.discounted_price
            amount += one_pro_value
        totalamount = amount + 40

        data = {
            'amount' : amount, 'totalamount' : totalamount 
        }
        return JsonResponse(data)
    
@login_required    
def wishlist(request):
    totalitem = 0
    wishitem = 0
    wishlist = Wishlist.objects.filter(user=request.user)

    if request.user.is_authenticated:
        user = request.user
        totalitem = len(Cart.objects.filter(user=user))
        wishitem = len(Wishlist.objects.filter(user=user))
    
    return render (request, 'app/wishlist.html', locals())

@login_required
def Pluswishlist(request):
    if request.method == 'GET' and request.user.is_authenticated:
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()

        data = {
            'message':'Wishlist Added Successfully'
        }
        return JsonResponse(data)


@login_required
def Minuswishlist(request):
    if request.method == 'GET' and request.user.is_authenticated:
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        w = Wishlist.objects.get(Q(product=product)& Q(user=user))
        w.delete()

        data = {
            'message':'Wishlist Removed Successfully' 
        }
        return JsonResponse(data)
    
#@login_required    
def search(request):
    query = request.GET['search']
    print(query)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        user = request.user
        totalitem = len(Cart.objects.filter(user=user))
        wishitem = len(Wishlist.objects.filter(user=user))
    product = Product.objects.filter(Q(title__icontains=query))
    
    return render (request, 'app/search.html', locals())


