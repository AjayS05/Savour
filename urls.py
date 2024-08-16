from unicodedata import name
from django.urls import path, include
from svr import views



urlpatterns = [
    path('',views.index, name='index'),
    path('user_login', views.user_login, name='user_login'),
    path('registration', views.registration, name='registration'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('AddItem', views.AddItem, name='AddItem'),
    path('Menu', views.Menu, name='Menu'),
    path('ContactUs', views.ContactUs, name='ContactUs'),
    path('cart', views.cart, name='cart'),
    path('order',views.order,name='order'),
    path('current_orders', views.current_orders, name="current_orders"),
    path('payment', views.payment, name='payment'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('profile', views.profile, name='profile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('invoice', views.invoice, name='invoice')
    
]
