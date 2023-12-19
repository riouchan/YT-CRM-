"""
URL configuration for crm1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home_dashboard'),
    path('products/', views.products,name='products'),
    path('customers/<str:pk_test>', views.customers,name='customers'),
    path('create_order/<str:pk>', views.create_order,name='createorder'),
    path('update_order/<str:pk>', views.update_order,name='updateorder'),
    path('delete_order/<str:pk>', views.delete_order,name='deleteorder'),
]
 