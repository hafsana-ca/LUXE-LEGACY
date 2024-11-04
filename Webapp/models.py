from django.db import models

# Create your models here.

class ContactDB(models.Model):
    Name = models.CharField(max_length=50,null=True,blank=True)
    Email = models.EmailField(max_length=50, null=True, blank=True)
    Message = models.TextField(max_length=500, null=True, blank=True)

class RegisterDB(models.Model):
    Username = models.CharField(max_length=50,null=True,blank=True)
    Email = models.EmailField(max_length=50,null=True,blank=True)
    Password1 = models.CharField(max_length=50,null=True,blank=True)
    Password2 = models.CharField(max_length=50,null=True,blank=True)

class CartDB(models.Model):
    User_Name = models.CharField(max_length=50,null=True,blank=True)
    Product_Name = models.CharField(max_length=50,null=True,blank=True)
    Quantity = models.IntegerField(null=True,blank=True)
    Price = models.IntegerField(null=True,blank=True)
    Total_Price = models.IntegerField(null=True,blank=True)

class OrderDB(models.Model):
    Name = models.CharField(max_length=50,null=True,blank=True)
    Email = models.EmailField(max_length=50,null=True,blank=True)
    Place = models.CharField(max_length=50,null=True,blank=True)
    Address = models.CharField(max_length=50,null=True,blank=True)
    Mobile = models.IntegerField(null=True,blank=True)
    Total_Price = models.IntegerField(null=True,blank=True)


class WishlistDB(models.Model):
    User_Name = models.CharField(max_length=50,null=True,blank=True)
    Image = models.ImageField(upload_to="Wishlist Images", null=True, blank=True)
    Product_Name = models.CharField(max_length=50,null=True,blank=True)
    Price = models.IntegerField(null=True,blank=True)
