from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfileInfo(models.Model):

    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Add any additional attributes you want
    
    contactno= models.PositiveBigIntegerField()
    
   

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username

class MenuCategory(models.Model):

    CatName= models.CharField(max_length=60)
    
    def __str__(self):
        return self.CatName


class MenuItems(models.Model):

    menuitems = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)

    ItemName= models.CharField(max_length=60)
    ItemRate= models.PositiveIntegerField()
    ItemImage= models.ImageField(upload_to='images/', default='userAccount.png')
    speciality=models.BooleanField(default=False)

    def __str__(self):
        return self.ItemName


class ContactUs(models.Model):

    FullName= models.CharField(max_length=60)
    Email= models.CharField(max_length=200)
    MobileNumber= models.PositiveBigIntegerField()
    feedbackType= models.CharField(max_length=20)
    QueryText= models.TextField()


    def __str__(self):
        return self.FullName

class Offer(models.Model):
    offer_code = models.CharField(max_length=10)
    OfferPercent = models.PositiveIntegerField(default=10)
    active = models.BooleanField()

    def __str__(self) -> str:
        return self.offer_code

class Cart(models.Model):
    ItemName = models.CharField(max_length=60)
    ItemQuant= models.PositiveIntegerField()
    ItemRate= models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.CharField(max_length=10, blank=True)
    def __str__(self) -> str:
        return self.ItemName


class Order(models.Model):

    items = models.TextField()
    served = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.PositiveIntegerField()
    bill_paid = models.BooleanField(default=False)
    table = models.PositiveIntegerField(default=1)
    personal_message = models.CharField(max_length=255, blank=True)
    p_req = models.BooleanField(default=False)
    p_type = models.CharField(max_length=20, choices=(('Cash', 'Cash'),('Card/Upi','Card/Upi'),('Online','Online')), default='Cash')
    o_type = models.CharField(max_length=8, choices=(('Takeout', 'Takeout'),('Dine-in','Dine-in')), default='Dine-in')

    def __str__(self):
        return str(self.table)    

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    razorpay_oid = models.CharField(max_length=255)
    razorpay_pid = models.CharField(max_length=255)