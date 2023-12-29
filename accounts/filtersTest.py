import django_filters
from django_filters import DateFilter, CharFilter

from .models import *



class OrderFilter(django_filters.FilterSet):

	product = django_filters.ModelChoiceFilter(field_name='product__name', 
                                        queryset=Product.objects.values_list('name', flat=True),
                                       	empty_label='Select Product',
                                       #label='product Name',  # Set label for the field
                                       widget=forms.Select(attrs={'class': 'form-control'})
	)

	class Meta:
		model = Order
		fields = ['customer__name', 'product', 'status']


class CustomerFilter(django_filters.FilterSet):
	class Meta:
		model = Customer
		fields = ['name', 'email', 'phone']

""" note = CharFilter(field_name='note', lookup_expr='icontains') """
 # New filters with choices
	""" choices = Order.objects.values_list('id','product')
	
	customer = django_filters.ChoiceFilter(
        field_name='customer_name',
        lookup_expr='icontains',
        choices=choices,
        widget=forms.Select(attrs={'class': 'form-control'})
	) """
	""" customer = django_filters.CharFilter(
     	lookup_expr='exact',
		widget = forms.TextInput(attrs={'class': 'form-control'})  # Applying Bootstrap classes
	) """
 
 """ start_date = django_filters.DateFilter(field_name="date_created", 
                                        lookup_expr='gte', 
                                        label='Start Date',
                                        widget=forms.DateTimeField(attrs={'class': 'form-control'})
	) """