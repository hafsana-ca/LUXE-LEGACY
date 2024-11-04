from django.db import models

# Create your models here.

class TextileDB(models.Model):
    Name = models.CharField(max_length=50,null=True,blank=True)
    Description = models.CharField(max_length=50, null=True, blank=True)
    Image = models.ImageField(upload_to="Category Images", null=True, blank=True)

class ProductDB(models.Model):
    Category_Name = models.CharField(max_length=50,null=True,blank=True)
    Product_Name = models.CharField(max_length=50, null=True, blank=True)
    Brand_Name = models.CharField(max_length=50, null=True, blank=True)
    Price = models.CharField(max_length=50, null=True, blank=True)
    Description = models.CharField(max_length=50, null=True, blank=True)
    Image1 = models.ImageField(upload_to="Product Images", null=True, blank=True)
    Image2 = models.ImageField(upload_to="Product Images", null=True, blank=True)
    Image3 = models.ImageField(upload_to="Product Images", null=True, blank=True)
