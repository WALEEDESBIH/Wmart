from django.shortcuts import render,redirect,HttpResponse
from WM_pp.models import Product,Catigories,Filter_Price,Brand,Color,Contact_us
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
import razorpay


def ABOUT(request):
    return render(request,'main/about.html')

def base(request):
    return render(request, 'main/base.html')




def Home(request):
    product = Product.objects.filter(status = 'Publish')
    context = {
        'product':product,
    }
    return render(request,'main/index.html',context)


def SEARCH(request):
    query = request.GET.get('query')
    product = Product.objects.filter(name__icontains=query)
    context = {
        'product': product
    }
    return render(request, 'main/search.html', context)

def PRODUCT_DETAILS_PAGE(request,id):
    prod = Product.objects.filter(id=id).first()
    context = {
        'prod': prod
    }
    return render(request, 'main/product_single.html',context)



def PRODUCT(request):
   product = Product.objects.filter(status = 'Publish')
   catigories = Catigories.objects.all()
   filter_price = Filter_Price.objects.all()
   color = Color.objects.all()
   brand = Brand.objects.all()

   CATID = request.GET.get('catigories')
   Filter_Price_ID = request.GET.get('filter_price')
   COLORID = request.GET.get('color')
   BRANDID = request.GET.get('brand')

   ATOZID= request.GET.get('ATOZ')
   ZTOAID = request.GET.get('ZTOA')
   LTOHID= request.GET.get('LTOH')
   HTOLID= request.GET.get('HTOL')
   NTODID= request.GET.get('NTOD')
   DTONID= request.GET.get('DTON')
   

   if CATID:
       product = Product.objects.filter(catigories = CATID,status = 'Publish')
   elif Filter_Price_ID:
       product = Product.objects.filter(filter_price = Filter_Price_ID,status = 'Publish')  
   elif COLORID:
       product = Product.objects.filter(color = COLORID,status = 'Publish')
   elif BRANDID:
       product = Product.objects.filter(brand = BRANDID,status = 'Publish')
   elif ATOZID:
       product = Product.objects.filter(status = 'Publish').order_by('name')
   elif ZTOAID:    
       product = Product.objects.filter(status = 'Publish').order_by('-name')
   elif LTOHID:
       product= Product.objects.filter(status = 'Publish').order_by('price')
   elif HTOLID:
       product= Product.objects.filter(status = 'Publish').order_by('-price')
   elif NTODID:
       product = Product.objects.filter(status = 'Publish',condition='New').order_by('-id')
   elif DTONID:
       product = Product.objects.filter(status = 'Publish',condition='Old').order_by('-id')               
   else:
        product = Product.objects.filter(status = 'Publish')
       


   context = {
        'product':product,
        'catigories':catigories,
        'filter_price':filter_price,
        'color':color,
        'brand':brand
    }
    
   return render(request,'main/product.html',context)

def CONTACT_US(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        contact = Contact_us(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )

        # Define the email subject, message, and sender
        email_subject = subject
        email_message = f"From: {name} <{email}>\n\nMessage:\n{message}"
        email_from = settings.EMAIL_HOST_USER

        try:
            # Send the email
            send_mail(
                subject=email_subject,
                message=email_message,
                from_email=email_from,
                recipient_list=['waleedesbih212@gmail.com'],  
                fail_silently=False,
            )
            contact.save()  # Save to the database if email was sent successfully
            return redirect('home')
        
        except Exception as e:
            print(f"Error sending email: {e}")  # For debugging
            return redirect('contact')
    return render(request,'main/contact.html')

def HandleRegister(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        customer = User.objects.create_user(username,email,pass1)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.save()
        return redirect('home')
    return render(request,'main/registration/auth.html')

def HandleLogin(request):
     if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return redirect('login')
     return render(request,'main/registration/auth.html')

def HandleLogout(request):
    logout(request)
    return redirect('home')




@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    return render(request, 'cart/cart_details.html')


@login_required(login_url="/login/")
def Check_out(request):
    return render(request, 'cart/checkout.html')


@login_required(login_url="/login/")
def PLACE_ORDER(request):
    if request.method=="POST":
       firstname = request.POST.get('firstname')

    return render(request, 'cart/placeorder.html')