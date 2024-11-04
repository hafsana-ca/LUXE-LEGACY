from django.shortcuts import render, redirect
from Webapp.models import ContactDB,RegisterDB, CartDB, OrderDB, WishlistDB
from Textileapp.models import TextileDB, ProductDB
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
import razorpay
import logging

# Create your views here.

def homepage(request):
    cat = TextileDB.objects.all()
    products = ProductDB.objects.filter(Category_Name="Womens Wear")
    products1 = ProductDB.objects.filter(Category_Name="Mens Wear")
    latest_products = ProductDB.objects.all().order_by('-id')[:3]
    return render(request, "Home.html", {'cat':cat, 'products':products, 'products1':products1, 'latest_products': latest_products} )

def product_list(request, category):
    products = ProductDB.objects.filter(Category_Name=category)
    return render(request, "product_list.html", {'products': products, 'category': category})

def about_page(request):
    cat = TextileDB.objects.all()
    return render(request, "About_Us.html", {'cat': cat})

def contact_page(request):
    cat = TextileDB.objects.all()
    return render(request, "Contact.html", {'cat': cat})

def contact_form(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('mail')
        msg = request.POST.get('message')

        obj = ContactDB(Name=name, Email=email, Message=msg)
        obj.save()
        return redirect(contact_page)

def all_products(request):
    cat = TextileDB.objects.all()
    products = ProductDB.objects.all()
    return render(request, "All_Products.html", {'cat': cat,'products':products})

def single_product(request, pro_id):
    cat = TextileDB.objects.all()
    product = ProductDB.objects.get(id=pro_id)

    # Check if the product is already in the user's wishlist
    username = request.session.get('username')
    is_in_wishlist = WishlistDB.objects.filter(User_Name=username, Product_Name=product.Product_Name).exists()

    context = {
        'product': product,
        'cat': cat,
        'is_in_wishlist': is_in_wishlist,  # Pass this to the template
    }

    return render(request, "Single_Product.html", context)


def single_product_name(request, product_name):
    product = get_object_or_404(ProductDB, Product_Name=product_name)
    return render(request, 'Single_Product.html', {'product': product})


def filtered_product(request, cat_name):
    cat = TextileDB.objects.all()
    data = ProductDB.objects.filter(Category_Name=cat_name)
    return render(request, "Filtered_Product.html", {'cat': cat,'data':data})

def web_login(request):
    return render(request, "Login.html")

def web_register(request):
    return render(request, "Register.html")

def register_details(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        obj = RegisterDB(Username=username, Email=email, Password1=password1, Password2=password2)
        obj.save()
        messages.success(request, "Registered successfully..!")
        return redirect(web_register)

def UserLogin(request):
    if request.method == "POST":
        username = request.POST.get('uname')
        password = request.POST.get('password')

        try:
            user = RegisterDB.objects.get(Username=username)

            if user.Password1 == password:
                request.session['username'] = username  # Store username in session
                messages.success(request, "Login successful!")
                return redirect('homepage')  # Redirect to homepage
            else:
                messages.warning(request, "Invalid username or password")
        except RegisterDB.DoesNotExist:
            messages.warning(request, "User not found")

    return render(request, 'login.html')



def user_logout(request):
    request.session.flush()  # Clears all session data
    logout(request)
    return redirect('web_login')


#single_product_page_addtocart
def add_cart(request):
    if request.method == "POST":
        username = request.POST.get('username')
        product_name = request.POST.get('productname')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        total_price = request.POST.get('total')

        obj = CartDB(User_Name=username, Product_Name=product_name, Quantity=quantity, Price=price, Total_Price=total_price)
        obj.save()
        messages.success(request, "Successfully Added..!")
        return redirect(homepage)
    return render(request, "Single_Product.html")

def cart_page(request):
    data = CartDB.objects.filter(User_Name=request.session['username'])
    cat = TextileDB.objects.all()
    sub_total=0
    total=0
    shipping = 0
    for i in data:
        sub_total += i.Total_Price

        if sub_total > 10000:
            shipping = 0    # Free shipping for orders above 10,000
        elif sub_total > 7000:
            shipping = 100  # Shipping charge of 100 for orders above 7,000
        elif sub_total > 5000:
            shipping = 150  # Shipping charge of 150 for orders above 5,000
        elif sub_total > 3000:
            shipping = 200  # Shipping charge of 200 for orders above 3,000
        elif sub_total > 1000:
            shipping = 250  # Shipping charge of 250 for orders above 1,000
        else:
            shipping = 300

        total=sub_total+shipping

    return render(request, "Cart.html", {'data':data,'cat':cat, 'sub_total':sub_total,
                                         'shipping':shipping, 'total':total})

def delete_item(request, dataid):
    x = CartDB.objects.filter(id=dataid)
    x.delete()
    messages.success(request,"Item Deleted..!")
    return redirect(cart_page)

def checkout_page(request):
    data = CartDB.objects.filter(User_Name=request.session['username'])
    cat = TextileDB.objects.all()

    sub_total = 0
    total = 0
    shipping = 0
    for i in data:
        sub_total += i.Total_Price

        if sub_total > 10000:
            shipping = 0  # Free shipping for orders above 10,000
        elif sub_total > 7000:
            shipping = 100  # Shipping charge of 100 for orders above 7,000
        elif sub_total > 5000:
            shipping = 150  # Shipping charge of 150 for orders above 5,000
        elif sub_total > 3000:
            shipping = 200  # Shipping charge of 200 for orders above 3,000
        elif sub_total > 1000:
            shipping = 250  # Shipping charge of 250 for orders above 1,000
        else:
            shipping = 300

        total = sub_total + shipping

    return render(request, "Checkout.html", {'data':data, 'cat':cat, 'sub_total':sub_total,
                                         'shipping':shipping, 'total':total})

def add_order(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        place = request.POST.get('place')
        address = request.POST.get('address')
        mobile = request.POST.get('phone')
        total_price = request.POST.get('total')

        obj = OrderDB(Name=name, Email=email, Place=place, Address=address,Mobile=mobile, Total_Price=total_price)
        obj.save()
        messages.success(request, "Ordered Successfully..!")
        return redirect(payment_page)
    return render(request, "Checkout.html")

def payment_page(request):
    cat = TextileDB.objects.all()
    customer = OrderDB.objects.order_by('-id').first()

    payy = customer.Total_Price
    amount = int(payy*100)
    payy_str = str(amount)

    for i in payy_str:
        print(i)

    if request.method == "POST":
        order_currency = 'INR'
        client = razorpay.Client(auth=('rzp_test_GgqJ5qD6i2W5HL ','a6zCHkUkHBHKgMCMnhvzK8Wi'))
        payment = client.order.create({'amount':amount, 'currency':order_currency})

    return render(request, "Payment.html", {'cat':cat, 'customer':customer, 'payy_str':payy_str })

def wishlist_page(request):
    data = WishlistDB.objects.filter(User_Name=request.session['username'])
    cat = TextileDB.objects.all()
    return render(request, "Wishlist.html", {'cat':cat, 'data':data})


def add_to_wishlist(request):
    if request.method == "POST":
        username = request.POST.get('username')
        product_name = request.POST.get('productname')
        price = request.POST.get('price')
        image_url = request.POST.get('image')
        pro_id = request.POST.get('pro_id')

        product = get_object_or_404(ProductDB, id=pro_id)

        if image_url == product.Image1.url:
            img = product.Image1
        else:
            img = None

        if img is None:
            messages.error(request, "Image not found or not available.")
            return redirect('single_product', pro_id=pro_id)

        obj = WishlistDB(User_Name=username, Image=img, Product_Name=product.Product_Name, Price=price)
        obj.save()

        messages.success(request, "Successfully Added to Wishlist!")
        return redirect('single_product', pro_id=pro_id)

    messages.error(request, "Invalid request.")
    return redirect('homepage')




def delete_wishlist(request, dataid):
    x = WishlistDB.objects.filter(id=dataid)
    x.delete()
    messages.success(request,"Item removed from wishlist..!")
    return redirect(wishlist_page)



def product_detail(request, product_id):
    product = ProductDB.objects.get(id=product_id)
    username = request.session.get('username')
    is_in_wishlist = WishlistDB.objects.filter(User_Name=username, Product_Name=product.Product_Name).exists()
    context = {
        'product': product,
        'is_in_wishlist': is_in_wishlist,
    }
    return render(request, 'Single_Product.html', context)




