from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# Create your views here.

def registrationPage(request):
    form = UserCreationForm()
    context = {}
    return render(request, 'accounts/register.html', context)

def loginPage(request):
    context = {}
    return render(request, 'accounts/login.html', context)


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customer = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    
    context = {'orders':orders, 
               'customers':customers,
               'total_customer':total_customer,
               'total_orders':total_orders,
               'delivered':delivered,
               'pending':pending,
               }
    
    return render(request, 'accounts/dashboard.html',context)

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/product.html',{'products':products})

def customers(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all() #to get foreign key of customer in order
    order_count = orders.count()
    
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'customer':customer,
               'orders':orders,
               'order_count':order_count,
               'myFilter':myFilter}
    return render(request, 'accounts/customer.html',context)

def create_order(request,pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'),extra=10)
    customer = Customer.objects.get(id=pk)
    #form = OrderForm(initial={'customer':customer}) #get the value customer data
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset':formset, 'customer':customer}
    return render(request, 'accounts/order_form.html',context)

def update_order(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid(): 
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'accounts/order_form.html',context)

def delete_order(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'orders':order}
    return render(request, 'accounts/delete_order.html',context)