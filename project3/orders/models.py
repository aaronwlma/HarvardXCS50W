from django.db import models
from django.utils import timezone

# Create your models here.
class Size(models.Model):
    size_name = models.CharField(max_length=64)

class Category(models.Model):
    item_name = models.CharField(max_length=64)

class Food(models.Model):
    dish = models.CharField(max_length=64)
    size = models.ForeignKey(Size, null=True, on_delete=models.SET_NULL, related_name="+")
    price = models.DecimalField(max_digits=9, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="foods")

class Customer(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    # orders = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, related_name="+")

class Order(models.Model):
    created_on = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, related_name="orders")
    foods = models.ManyToManyField(Food, blank=True, related_name="+")
    PENDING = 'Pending'
    RECEIVED = 'Received'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (RECEIVED, 'Received'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
    ]
    status = models.CharField(max_length=64, choices=STATUS_CHOICES, default=PENDING)
