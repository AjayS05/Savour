from django import forms
from django.contrib.auth.models import User

from .models import Cart, MenuCategory, MenuItems, Offer, Order, Payment, UserProfileInfo, ContactUs
from django.contrib import admin
# Register your models here.

admin.site.register(UserProfileInfo)
admin.site.register(MenuCategory)
admin.site.register(MenuItems)
admin.site.register(ContactUs)
admin.site.register(Cart)
admin.site.register(Offer)
admin.site.register(Order)
admin.site.register(Payment)