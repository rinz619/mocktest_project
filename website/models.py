from django.db import models

# Create your models here.

class Customers(models.Model):
    customer_id  = models.TextField(unique=True)
    first_name = models.TextField(null=True, blank=True)
    last_name = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    phone = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Destinations(models.Model):
    destination_id  = models.TextField(unique=True)
    destination_name = models.TextField(null=True, blank=True)
    country = models.TextField(null=True, blank=True)
    popular_seasion = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Bookings(models.Model):
    book_id  = models.TextField(unique=True)
    customer_id = models.ForeignKey('Customers',on_delete=models.SET_NULL, null=True, blank=True)
    destination_id = models.ForeignKey('Destinations',on_delete=models.SET_NULL, null=True, blank=True)
    booking_date = models.DateField(null=True, blank=True)
    passengers = models.IntegerField(default=0)
    costperpassenger = models.DecimalField(max_digits=8, decimal_places=2)
    totalcost = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)