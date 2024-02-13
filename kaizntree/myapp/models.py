from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=50, default='')  # Provide a default value here
    last_name = models.CharField(max_length=50,default='')
    password = models.CharField(max_length=128,default='abcde123')
    email = models.EmailField(max_length=254, blank=True,default='')
    business_name = models.CharField(max_length=100, blank=True,default='')
    phone_number = models.CharField(max_length=20, blank=True,default='')
    country = models.CharField(max_length=50, blank=True,default='')
    nature_of_operations = models.CharField(max_length=100, blank=True,default='')
    membership = models.CharField(max_length=50, blank=True,default='')
    # Define primary key
    username = models.CharField(max_length=50, primary_key=True)
class Category(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    keywords = models.CharField(max_length=255, blank=True)
    default_location = models.CharField(max_length=100, blank=True)
class Items(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sku = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    tags = models.CharField(max_length=255,null=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0,null=True)
    in_stock = models.BooleanField(default=0,null=True)
    net_stock = models.IntegerField(default=0,null=True)
    available_stock = models.IntegerField(default=0)
    quantity_sold_this_month = models.IntegerField(default=0,null=True)
    quantity_sold_last_month = models.IntegerField(default=0,null=True)