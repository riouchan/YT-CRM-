from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.name
 
class Customer(models.Model):
    name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.name
    

@receiver(pre_save, sender=Customer)
def format_customer_fields(sender, instance, **kwargs):
    instance.name = instance.name.capitalize()  # Capitalize the name

class Product(models.Model):
    CATEGORY = (
        ('in door', 'in door'),
        ('out door', 'out door'),
    )
    name = models.CharField(max_length=255, null=True)
    price =models.FloatField(null=True)
    category = models.CharField(max_length=255, null=True, choices=CATEGORY)
    description = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tag = models.ManyToManyField(Tag)
    
    def __str__(self):
        return self.name
    
    
class Order(models.Model):
    class StatusChoices(models.TextChoices):
        Pending = "Pending"
        Out_of_Delivery = "Out of Delivery"
        Delivered = "Delivered"
    
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL) 
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL) 
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(
        max_length=255, null=True, choices=StatusChoices.choices)
    note =  models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.status

  