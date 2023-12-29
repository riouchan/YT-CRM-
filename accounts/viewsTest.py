from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.db.models import Q

from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter, CustomerFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.


@unauthenticated_user
def registrationPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, "Account was created for " + username)
            return redirect("login")

    context = {"form": form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home_dashboard')
        else:
            messages.info(request, "Username or Password is incorrect ")

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect("login")


# filter function  filter by request (item exist in the page)
""" def home(request):
    customer = Customer.objects.all()
    title_contains_query = request.GET.get('title_contains')
    id_exact_query = request.GET.get('id_exact')
    title_or_author_query = request.GET.get('title_or_author')
    
    if title_contains_query != '' and title_contains_query is not None:
        qs = qs.filter(title__icontains=title_contains_query)
        
    return customer
    """


def is_valid_queryparam(param):
    return param != '' and param is not None


def filter(request):
    qs = Order.objects.all()
    products = Product.objects.all()
    customer_query = request.GET.get('customer_name')
    status = request.GET.get('status')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    product = request.GET.get('product')
    status = Order.STATUS

    if is_valid_queryparam(customer_query):
        qs = qs.filter(Q(note__icontains=customer_query)
                       | Q(customer__name__icontains=customer_query)
                       ).distinct()

    if is_valid_queryparam(date_min):
        qs = qs.filter(date_created__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(date_created__lt=date_max)

    if is_valid_queryparam(product) and product != 'Choose Product':
        qs = qs.filter(product__name=product)

    if is_valid_queryparam(status) and status != 'Status':
        qs = qs.filter(status=status)

    return qs


@login_required(login_url="login")
# @admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customer = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    myOrderFilter = OrderFilter(request.GET, queryset=orders)
    orders = myOrderFilter.qs
    myCustomerFilter = CustomerFilter(request.GET, queryset=customers)
    customers = myCustomerFilter.qs
    order_filter = OrderFilter(request.GET, queryset=Order.objects.all())
    order_status_filter = OrderFilter(
        request.GET, queryset=Order.objects.values_list('status', flat=True))
    customers = Customer.objects.all()
    orders = Order.objects.all()

    context = {'order_filter_form': order_filter.form,
               'order': order_filter.qs,
               'order_status_filter_form': order_status_filter.form,
               'order_status_filter_qs': order_status_filter.qs,
               'customers': customers,
               'orders': orders,
               'orders': orders,
               'customers': customers,
               'total_customer': total_customer,
               'total_orders': total_orders,
               'delivered': delivered,
               'pending': pending,
               'myOrderFilter': myOrderFilter,
               'myCustomerFilter': myCustomerFilter,
               }

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def userPage(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_customer = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders,
               'customers': customers,
               'total_customer': total_customer,
               'total_orders': total_orders,
               'delivered': delivered,
               'pending': pending,
               }

    return render(request, 'accounts/user.html', context)


@login_required(login_url="login")
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/product.html', {'products': products})


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "kanrisya"])
def customers(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()  # to get foreign key of customer in order
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'customer': customer,
               'orders': orders,
               'order_count': order_count,
               'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context)


@login_required(login_url="login")
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    # form = OrderForm(initial={'customer':customer}) #get the value customer data
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset': formset, 'customer': customer}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "staff"])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "staff"])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'orders': order}
    return render(request, 'accounts/delete_order.html', context)