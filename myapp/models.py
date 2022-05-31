from itertools import product
from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

#this is a new product
# Create your models here.
class Product(models.Model): #create a Model class
    #id = models.AutoField(primary_key=True)

    #show properties names
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('myapp:products')
    
    seller_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.CharField(max_length=200)
    image = models.ImageField(blank=True,upload_to='img')


class OrderDetail (models.Model):
    
     #show properties names
    def __str__(self):
        return self.customer_username
    
    customer_username = models.CharField(max_length=200)
    product = models.ForeignKey(to='Product', on_delete=models.PROTECT) # prevent deletion of Product
    amount = models.IntegerField()
    stripe_payment_intent = models.CharField(max_length=200)
    has_paid = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)
    