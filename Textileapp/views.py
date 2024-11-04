from django.shortcuts import render, redirect
from Textileapp.models import TextileDB, ProductDB
from Webapp.models import ContactDB,RegisterDB
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout

# Create your views here.

def textile_index(request):
    today = datetime.datetime.now()
    x = today.date()
    return render(request, "index.html", {'today':today , 'x':x})

def textile_page(request):
    return render(request, "Add_Categories.html")

def add_category(request):
    if request.method == "POST":
        a = request.POST.get('Name')
        b = request.POST.get('Description')
        c = request.FILES['Image']

        obj = TextileDB(Name=a, Description=b, Image=c)
        obj.save()
        messages.success(request, "Category saved successfully..!")
        return redirect(add_category)

    else:
        return render(request, "Add_Categories.html")

def view_category(request):
    data = TextileDB.objects.all()
    return render(request, "View_Category.html", {'data':data})

def edit_category(request,dr_id):
    data = TextileDB.objects.get(id=dr_id)
    return render(request,"Edit_Category.html", {'data':data})


def delete_category(request,dr_id):
    x = TextileDB.objects.filter(id=dr_id)
    x.delete()
    messages.error(request, "Category deleted successfully..!")
    return redirect(view_category)

def update_category(request,data_id):
    if request.method == "POST":
        a = request.POST.get('Name')
        b = request.POST.get('Description')
        try:
            img = request.FILES['Image']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file = TextileDB.objects.get(id=data_id).Image

        TextileDB.objects.filter(id=data_id).update(Name=a, Description=b, Image=file)
        return redirect(view_category)

def product_page(request):
        category = TextileDB.objects.all()
        return render(request, "Add_Products.html", {'category':category})

def add_products(request):
    if request.method == "POST":
        a = request.POST.get('Category_Name')
        b = request.POST.get('Product_Name')
        c = request.POST.get('Brand_Name')
        d = request.POST.get('Price')
        e = request.POST.get('Description')
        f = request.FILES['Image1']
        g = request.FILES['Image2']
        h = request.FILES['Image3']

        obj = ProductDB(Category_Name=a, Product_Name=b, Brand_Name=c, Price=d,Description=e, Image1=f, Image2=g, Image3=h)
        obj.save()
        return redirect(product_page)

    else:
        return render(request, "Add_Products.html")

def view_product(request):
    data = ProductDB.objects.all()
    return render(request, "View_Products.html", {'data':data})

def edit_product(request, dr_id):
    data = ProductDB.objects.get(id=dr_id)
    categories = TextileDB.objects.all()  # Assuming you want to list categories
    return render(request, "Edit_Products.html", {'data': data, 'category': categories})


def delete_product(request,dr_id):
    x = ProductDB.objects.filter(id=dr_id)
    x.delete()
    return redirect(view_product)

def update_product(request,data_id):
    if request.method == "POST":
        a = request.POST.get('Category_Name')
        b = request.POST.get('Product_Name')
        c = request.POST.get('Brand_Name')
        d = request.POST.get('Price')
        e = request.POST.get('Description')
        try:
            img = request.FILES['Image1']
            fs = FileSystemStorage()
            file1 = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file1 = ProductDB.objects.get(id=data_id).Image1

        try:
            img = request.FILES['Image2']
            fs = FileSystemStorage()
            file2 = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file2 = ProductDB.objects.get(id=data_id).Image2

        try:
            img = request.FILES['Image3']
            fs = FileSystemStorage()
            file3 = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file3 = ProductDB.objects.get(id=data_id).Image3

        ProductDB.objects.filter(id=data_id).update(Category_Name=a, Product_Name=b, Brand_Name=c, Price=d,Description=e, Image1=file1, Image2=file2, Image3=file3)
        return redirect(view_product)

def adminlogin(request):
    return render(request, "Admin_Login.html")

def admin_login(request):
    if request.method == "POST":
        un = request.POST.get('username')
        pwd = request.POST.get('password')

        user = authenticate(request, username=un, password=pwd)

        if user is not None and user.is_staff:  # Check if the user is a staff/admin
            login(request, user)  # Django's built-in login function
            request.session['username'] = user.username  # Store username in session
            messages.success(request, "Login Successful!")
            return redirect('textile_index')  # Redirect after successful login
        else:
            messages.warning(request, "Invalid username or password")
            return redirect('adminlogin')  # Redirect back to login on failure

    return render(request, 'admin_login.html')


def admin_logout(request):
    request.session.flush()  # Clears all session data
    logout(request)
    return redirect('adminlogin')

def contact_pg(request):
    return render(request, "Contact_Details.html")

def view_contact(request):
    data = ContactDB.objects.all()
    print(data)
    return render(request, "Contact_Details.html", {'data':data})

def delete_contact(request,dr_id):
    x = ContactDB.objects.filter(id=dr_id)
    x.delete()
    return redirect(contact_pg)

def view_registration(request):
    data = RegisterDB.objects.all()
    print(data)
    return render(request, "Registration_Details.html", {'data':data})

def delete_registration(request,dr_id):
    x = RegisterDB.objects.filter(id=dr_id)
    x.delete()
    return redirect(view_registration)