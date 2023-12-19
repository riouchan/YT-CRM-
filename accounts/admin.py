from django.contrib import admin
from .models import Customer, Product, Order, Tag
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'date_created')
    list_display_links = ('id','name', 'email')
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'status')
    list_display_links = ('customer', 'product', 'status')

admin.site.register(Customer,CustomerAdmin)
admin.site.register(Product)
admin.site.register(Order,OrderAdmin)
admin.site.register(Tag)