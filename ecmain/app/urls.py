from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='app-home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('category/<slug:catgry>/', views.CategoryView.as_view(), name='category'),
    path('category-title/<str:title>/', views.CategoryTitle.as_view(), name='category-title'),
    path('product-detail/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),

    path('add-to-cart/', views.AddToCart,name='add_to_cart'),
    path('cart/', views.ShowCart,name='showcart'),
    path('checkout/', views.checkout.as_view(), name='checkout'),
    path('paymentdone/', views.paymentDone, name='paymentdone'),
    path('orders/', views.orders, name='orders'),

    path('pluscart/', views.PlusCart),
    path('minuscart/', views.minusCart),
    path('removecart/', views.removeCart),
    
    path('wishlist/', views.wishlist, name='wishlist'),
    path('pluswishlist/', views.Pluswishlist),
    path('minuswishlist/', views.Minuswishlist),

    path('search/', views.search, name='search'),

]
