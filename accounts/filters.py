from django import forms
import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class OrderFilter(django_filters.FilterSet):
	
	start_date = DateFilter(field_name='date_created',
							widget= forms.DateInput(format='%d-%b-%Y', attrs={'class': 'form-control', 'placeholder': 'Start Date From', 'type': 'text','onfocus': "(this.type='date')" }),
							lookup_expr='gt', label='Start Date')
	end_date = DateFilter(field_name='date_created',
							widget= forms.DateInput(format='%d-%b-%Y', attrs={'class': 'form-control', 'placeholder': 'Start Date To', 'type': 'text','onfocus': "(this.type='date')" }),
							lookup_expr='lt', label='End Date')
	
	customer = django_filters.CharFilter(field_name='customer__name', 
                                      	lookup_expr='icontains',
                                       #label='Customer Name'  # Set label for the field
                                       widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Customer Name'})
	)

	product = django_filters.ModelChoiceFilter(field_name='product__name', 
                                       	empty_label='Select Product',
                                        queryset=Product.objects.all(),
                                       #label='product Name'  # Set label for the field
                                       widget=forms.Select(attrs={'class': 'form-control'})
	)
	
	status = django_filters.ChoiceFilter(field_name='status', 
                                       	empty_label='Status',
                                        choices=Order.STATUS,
                                       #label='product Name'  # Set label for the field
                                       widget=forms.Select(attrs={'class': 'form-control'})
	)
 
	class Meta:
		model = Order
		""" fields = {'customer' : ['exact'],
            	'product': ['exact']} """
		fields = [	'customer', 
            		'product', 
           	 		'status',
					'note',
					'start_date',
					'end_date',
           		 	]
		"""widget = {'customer' :forms.TextInput(
      				attrs={'class': 'form-control', 
                           'placeholder':'Customer Name'})
				} """

		exclude = ['date_created']

		""" filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
        } """
  
		
		
class CustomerFilter(django_filters.FilterSet):
	class Meta:
		model = Customer
		fields = ['name', 'email', 'phone']
