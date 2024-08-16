from pickle import NONE
import profile
from re import T
from sre_constants import CATEGORY_SPACE
from unicodedata import category
from django.shortcuts import render
import random
from .models import Cart, MenuItems, UserProfileInfo, MenuCategory, User, Offer,Order, Payment
from .forms import ContactUsForm, ItemForm, UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, HttpRequest,HttpResponseRedirect
from django.core import serializers
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponseBadRequest
import re
# Create your views here.

def index(request):
    speciality=[]
    special = MenuItems.objects.filter(speciality=True)
    
    for i in special:
        speciality.append(i)
    
    
    if len(speciality) > 2:
        speciality1 = random.choice(speciality).ItemImage
        
        speciality2 = random.choice(speciality).ItemImage

        speciality3 = random.choice(speciality).ItemImage
        
        while speciality1==speciality2:
            speciality2= random.choice(speciality).ItemImage

        while speciality1==speciality3:
            speciality3= random.choice(speciality).ItemImage

        while speciality2==speciality3:
            speciality3= random.choice(speciality).ItemImage

        '''def checksame(sp1, sp2):
            if sp1 == sp2:
                sp2 = random.choice(speciality).ItemImage
                if sp1 == sp2:
                    checksame()        
        checksame(speciality1, speciality2)
        
        speciality3 = random.choice(speciality).ItemImage
        checksame(speciality1, speciality3)
        checksame(speciality2, speciality3)
'''
        
    elif len(speciality) == 1:
        speciality2 = speciality1
        speciality3 = speciality1
    print(speciality1)
    
    burger = MenuCategory.objects.get(CatName='Burger')
    burger = MenuItems.objects.filter(menuitems=burger)
    sandwich = MenuCategory.objects.get(CatName='Sandwich')
    sandwich = MenuItems.objects.filter(menuitems=sandwich)
    pizza = MenuCategory.objects.get(CatName='Pizza')
    pizza = MenuItems.objects.filter(menuitems=pizza)
    pasta = MenuCategory.objects.get(CatName='Pasta')
    pasta = MenuItems.objects.filter(menuitems=pasta)
    side = MenuCategory.objects.get(CatName='Sides')
    side = MenuItems.objects.filter(menuitems=side)
    

    burgers = []
    sandwiches = []
    pizzas = []
    pastas = []
    sides = []
    
    for i in burger:
        burgers.append(i)
    for i in sandwich:
        sandwiches.append(i)
    for i in pizza:
        pizzas.append(i)
    for i in pasta:
        pastas.append(i)
    for i in side:
        sides.append(i)

    if len(burgers)>0:
        bg = random.choice(burgers).ItemImage
    if len(sandwiches)>0:
        sw = random.choice(sandwiches).ItemImage
    if len(pizzas)>0:
        pz = random.choice(pizzas).ItemImage
    if len(pastas)>0:
        ps = random.choice(pastas).ItemImage
    if len(sides)>0:
        sd = random.choice(sides).ItemImage

    my_dict = {"special1":speciality1,'special2':speciality2, 'special3':speciality3, 'burger':bg, 'sandwich':sw,'pizza':pz,'pasta':ps,
    'sides':sd}
    return render(request, 'Savour.html', context=my_dict)

def user_login(request):
    if request.method == 'POST':
        
            username = request.POST.get('username')
            password = request.POST.get('password')


            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return HttpResponse("Your account is not active.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
                return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'user_login.html', {})


@login_required
def user_logout(request):

    logout(request)
    return HttpResponseRedirect(reverse('index'))

def registration(request):
    registered = False
    
    pasw = True
    contact = True
    if request.method == 'POST':
        upper = False
        symbol = False
        digit = False
        pasw = False
        contact = False
        user_form = UserForm(data=request.POST)
        UserProfile = UserProfileInfoForm(data=request.POST)
       
        if user_form.is_valid() and UserProfile.is_valid() : 
            user = user_form.save(commit=False)
            for i in user.password:
                if i.isupper():
                    upper = True
                if i in ['@','.','+','-','_']:
                    symbol = True
                if i in ['1','2','3','4','5','6','7','8','9','0']:
                    digit = True
            if upper and symbol and digit:
                pasw = True
            profile= UserProfile.save(commit= False)
            r = re.search("^([9]{1})([234789]{1})([0-9]{8})$", str(profile.contactno))
            if r is not None:
                contact = True
            if contact and pasw:
                
                user.set_password(user.password)
                user.save() 
            
                profile.user= user
                profile.save()
                registered = True
        else:     
            print(user_form.errors, UserProfile.errors)
            
    else:
        user_form = UserForm()
        UserProfile= UserProfileInfoForm()
    return render(request,'registration.html',{'user_form':user_form,'registered':registered, 'UserProfileInfoForm':UserProfile,'pasw':pasw,'contact':contact})

def AddItem(request):
    added= False

    if request.method=='POST':
        item_form= ItemForm(request.POST, request.FILES)

        if item_form.is_valid():
            for i in MenuCategory.objects.values_list('CatName'):
                print(i)
            item= item_form.save(commit=False)
            
            category=MenuCategory.objects.get(CatName=request.POST.get("menuitems"))
            
            item.menuitems=category
            
            item.save()
            added= True
        
        else:
            print(item_form.errors)
        
    else:
        item_form=ItemForm()


    return render(request, 'uploadMenu.html', {'item_form': item_form, 'added': added})


def Menu(request):
    if request.user.is_authenticated:
        icart = []
        cart = None
        post = False
        if request.method== "POST":
            cart = []
            items = serializers.serialize('python',Cart.objects.filter(user=User.objects.get(username=request.user.username)))
            for i in items:
                f = i['fields']
                cart.append([f['ItemName'], f['ItemQuant']])
                icart = []
                
                post= True
            for i in cart:
                    icart.append(i[0])


        data = serializers.serialize( "python", MenuCategory.objects.all() )
        category = []
        for i in data:
            category.append([i['fields']['CatName'], i['pk']])
        menu= []
        menudata = serializers.serialize( "python", MenuItems.objects.all() )
        for i in menudata:
            menu.append([i['fields']['ItemName'],i['fields']['ItemImage'], i['fields']['ItemRate'],i['fields']['menuitems']])
        
        return render(request, 'Menu.html', context={'category':category, 'menu':menu, 'cart':cart, 'post':post, 'icart':icart})
    else:
        return HttpResponseRedirect(reverse('svr:user_login'))

def ContactUs(request):
    contact = False
    mobile = True
    if request.method == 'POST':
        mobile = False
        contact_form= ContactUsForm(data=request.POST)

        if contact_form.is_valid():
            contactf= contact_form.save(commit=False)
            r = re.search("^([9]{1})([234789]{1})([0-9]{8})$", str(contactf.MobileNumber))
            if r is not None:
                mobile = True
                contactf.save()
                contact = True
        else:
            print(contact_form.errors)
    
    else:
        contact_form= ContactUsForm()

    return render(request, 'ContactUs.html',context= {'contact_form': contact_form, 'contact':contact, 'mobile':mobile})


def cart(request):
    cart = []
    isoffer = None
    username = request.user.username
    user = User.objects.get(username=username)
    grand_total = 0
    cart_empty = False
    if request.method == 'POST':
        
        if 'item' in request.POST:
            
            name = request.POST.get('item', False)
            get = Cart.objects.get(ItemName = name, user=user)
            get.delete()
            try:
                
                data = serializers.serialize('python', Cart.objects.filter( user=user))
                for i in data:
                    f = i['fields']
                    total = f['ItemQuant']*f['ItemRate']
                    cart.append([f['ItemName'], f['ItemQuant'], f['ItemRate'], total])
                    grand_total+= total
            except: 
                cart = [['-','-','-','-']]
        elif 'claim' in request.POST:

            name = request.POST.get('offer', False)
            offer = None
            try:
                offer = Offer.objects.get(offer_code=name,active=True)
            except:
                isoffer = False
           
            if offer is not None:
                try:

                    carts = Cart.objects.filter(user=user)
                    for i in carts:
                        
                        if i.offer == offer.offer_code:
                            isoffer = True
                            continue
                        elif i.offer != '':

                            menu = MenuItems.objects.get(ItemName=i.ItemName)
                            i.ItemRate = menu.ItemRate
                            
                        
                        i.ItemRate=int(i.ItemRate-(i.ItemRate*(offer.OfferPercent/100)))
                        
                        i.offer = offer.offer_code
                        i.save()
                except:
                    isoffer = True
                
            try:
            
                data = serializers.serialize('python', Cart.objects.filter( user=user))
                for i in data:
                    f = i['fields']
                    total = f['ItemQuant']*f['ItemRate']
                    cart.append([f['ItemName'], f['ItemQuant'], f['ItemRate'], total])
                    grand_total+= total
            except: 
                cart = [['-','-','-','-']]
        
        else:
            cart_items = MenuItems.objects.values_list('ItemName')
            
            for i in cart_items:
                q = int(request.POST.get(i[0]))
                
                if q > 0:
                    rate = MenuItems.objects.get(ItemName= i[0]).ItemRate
                    
                    try:
                        
                        get = Cart.objects.get(ItemName = i[0], user=user)
                        get.ItemQuant=q
                        get.ItemRate=rate
                        get.save()
                        q = get.ItemQuant
                
                        
                    except:

                        Cart.objects.get_or_create(ItemName = i[0], ItemQuant = q, ItemRate = rate, user=User.objects.get(username=request.user.username))
                
                    cart.append([i[0], q, rate, q*rate])
                    grand_total += q*rate
                else:
                    try:

                        get = Cart.objects.get(ItemName = i[0], user=user)
                        get.delete()
                    except:
                        pass
        
    else:
        try:
            
            data = serializers.serialize('python', Cart.objects.filter( user=user))
            for i in data:
                f = i['fields']
                total = f['ItemQuant']*f['ItemRate']
                cart.append([f['ItemName'], f['ItemQuant'], f['ItemRate'], total])
                grand_total+= total
        except: 
            cart = [['-','-','-','-']]
    return render(request,'cart.html', context={'cart':cart, 'isoffer':isoffer, 'grand_total':grand_total,'cart_Empty':cart_empty})


def order(request):
    username = request.user.username
    user = User.objects.get(username=username)
    cart_empty= False
    grand_total= 0
    if request.method == 'POST':
        items = ''
        table = request.POST.get('table',False)
        message = request.POST.get('personal', False)
        o_type = request.POST.get('type', False)
        t_occ = False
        try:
            t = Order.objects.get(table=table, bill_paid = False)
            if t is not None:
                t_occ = True
        except:
            if t_occ == False:
                try:
                    data = serializers.serialize('python', Cart.objects.filter( user=user))
                    for i in data:
                        f = i['fields']
                        total = int(f['ItemQuant'])*int(f['ItemRate'])
                        
                        items += f['ItemName']+'-'+ str(f['ItemQuant'])+','     
                                
                        grand_total+= total
                
                except:
                    cart_empty =True
                if items != '':

                    Order.objects.create(items=items, total=grand_total,user=user, table=table,o_type=o_type,
                    personal_message=message)
                    cart = Cart.objects.filter(user=user)
                    for i in cart:
                        i.delete()
                else:
                    cart_empty=True 
    
        
        
    return render(request, 'order.html',context={'cart_empty':cart_empty, 't_occ':t_occ})



def current_orders(request):
    
    if request.user.is_staff:
        if request.method=='POST':
            if 'paid' in request.POST:
                order = Order.objects.get(id=request.POST.get('id',''))
                order.bill_paid = True
                order.p_req = False
                order.save()
            id1 = request.POST.get('id', False)
            order = Order.objects.get(id=id1)
            order.served = True
            order.save()
        try:
            order = serializers.serialize('python', Order.objects.filter(served=False))
            orders =[]
            for i in order:
                f = i['fields']
                orders.append([i['pk'],f['items'].split(','),f['table'],f['o_type'], f['personal_message'], f['total']])
        except:
            orders= []
        try:
            all = serializers.serialize('python', Order.objects.all())
            alls =[]
            for i in all:
                f = i['fields']
                alls.append([i['pk'],f['items'].split(','),f['table'],f['o_type'],f['bill_paid'],f['p_req'],f['p_type'], f['personal_message'], f['total']])
        except:
            alls= []
    return render(request,'serve.html', context={'orders':orders, 'alls':alls})


razorpay_client = razorpay.Client(

auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
 

def payment(request):
    context = {}
    display = ''
    
    if request.method == 'POST':
        if 'oid' in request.POST:
            request.session['oid'] = request.POST.get('oid','')
            display = ''
        elif 'cash' in request.POST:
            order = Order.objects.get(id=request.session['oid'])
            order.p_req=True
            order.p_type = 'Cash'
            order.save()
            display = 'Your payment request has been generated, after completion you can check your invoice from "myacccount"'
        elif 'card' in request.POST:
            order = Order.objects.get(id=request.session['oid'])
            order.p_req=True
            order.p_type = 'Card/Upi'
            order.save()
            display = 'Your payment request has been generated, after completion you can check your invoice from "myacccount"'

        elif 'razor' in request.POST:
            order = Order.objects.get(id=request.session['oid'])
            order.p_req=True
            order.p_type = 'Online'
            order.save()
            currency = 'INR'

            amount = int(order.total)*100  
            request.session['amount'] = amount

            # Create a Razorpay Order

            razorpay_order = razorpay_client.order.create(dict(amount=amount,

                                                            currency=currency,

                                                            payment_capture='0'))
        

            # order id of newly created order.

            razorpay_order_id = razorpay_order['id']

            callback_url = 'paymenthandler/'
        

            # we need to pass these details to frontend.

            

            context['razorpay_order_id'] = razorpay_order_id
            request.session['razorpay_order_id'] = razorpay_order_id
            context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
            request.session['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
            context['razorpay_amount'] = amount
            
            context['currency'] = currency

            context['callback_url'] = callback_url
            display = ''
    context['display'] = display 
    return render(request, 'payment.html', context=context)
    
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.

@csrf_exempt
def paymenthandler(request):
 

    # only accept POST request.

    if request.method == "POST":

        try:

           

            # get the required parameters from post request.

            payment_id = request.POST.get('razorpay_payment_id', '')

            razorpay_order_id = request.POST.get('razorpay_order_id', '')

            signature = request.POST.get('razorpay_signature', '')

            params_dict = {

                'razorpay_order_id': razorpay_order_id,

                'razorpay_payment_id': payment_id,

                'razorpay_signature': signature

            }
 

            # verify the payment signature.

            result = razorpay_client.utility.verify_payment_signature(

                params_dict)

            if result is not None:
                order = Order.objects.get(id=request.session['oid'])
                amount =  request.session['amount']

                try:
 

                    # capture the payemt

                    razorpay_client.payment.capture(payment_id, amount)
                    order.p_req = False
                    order.bill_paid = True
                    order.save()
                    Payment.objects.create(order=order, razorpay_oid = razorpay_order_id, razorpay_pid = payment_id)

                    # render success page on successful caputre of payment

                    return render(request, 'paymentsuccess.html')

                except:
 

                    # if there is an error while capturing payment.

                    return render(request, 'paymentfail.html')

            else:
 

                # if signature verification fails.

                return render(request, 'paymentfail.html')

        except:
 

            # if we don't find the required parameters in POST data

            return HttpResponseBadRequest()

    else:

       # if other than POST request is made.

        return HttpResponseBadRequest()
 

def profile(request):
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        
        info = UserProfileInfo.objects.get(user=user)

        my_dict = {}

        my_dict['username'] = username
        my_dict['email'] = user.email
        my_dict['phone'] = info.contactno

        try:
            order = serializers.serialize('python', Order.objects.filter(user=user))
            orders = []
            for i in order:
                f = i['fields']
                orders.append([i['pk'],f['items'].split(','),f['table'],f['o_type'], f['bill_paid'], f['personal_message'], f['total']])
                
        except:
            orders = None
        my_dict['orders'] = orders

        return render(request, 'profile.html', context=my_dict)
    else:
        return HttpResponseRedirect(reverse('svr:user_login'))


def edit_profile(request):
    if request.method =='POST':

        
        username = request.user.username
        user =User.objects.get(username=username)
        info = UserProfileInfo.objects.get(user=user)
        
        email = request.POST.get('email', False)
        phone = request.POST.get('phone', False)
        
        
        
        username = request.POST.get('username', False)
        user.username=username
        user.email=email
        user.save()
        
        
        info.contactno=phone
        
       
        info.save()
        username = request.user.username
        user =User.objects.get(username=username)
        info = UserProfileInfo.objects.get(user=user)

        my_dict = {}

        my_dict['username'] = username
        my_dict['email'] = user.email
        my_dict['phone'] = info.contactno
         
    else:
        username = request.user.username
        user = User.objects.get(username=username)
        
        info = UserProfileInfo.objects.get(user=user)

        my_dict = {}

        my_dict['username'] = username
        my_dict['email'] = user.email
        my_dict['phone'] = info.contactno
   

        
    return render(request, 'edit_profile.html', context=my_dict)


def invoice(request):
    data = []
    if request.method == 'POST':
        id = request.POST.get('id','')

        
        order = Order.objects.get(id=id)
        items = order.items.split(',')
        total = order.total
        type = order.p_type
        data = [id, items, total, type]

    return render(request, 'invoice.html', context = {'data':data})