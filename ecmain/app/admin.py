from django.contrib import admin
from .models import Product, Cart, Payment, Orderplaced, Wishlist

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'category', 'product_image']

@admin.register(Cart)
class CartItemModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'products', 'quantity']


@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'razorpay_order_id', 'razorpay_payment_status', 'razorpay_payment_id', 'paid']

@admin.register(Orderplaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'payment']

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product']