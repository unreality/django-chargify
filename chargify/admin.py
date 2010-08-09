from django.contrib import admin
from chargify.models import *


from django import forms

class CustomerAdminForm(forms.ModelForm):
    
    first_name = forms.CharField(
        max_length = 90,
        widget = forms.TextInput(
            attrs = {"style": "width: 50%;"},
        ),
        help_text = u"Optional. Override the User's first name",
        required=False,
    )
    
    last_name = forms.CharField(
        widget = forms.TextInput(
            attrs = {"style": "width: 50%;"},
        ),
        help_text = u"Optional. Override the User's last name",
        required=False,
    )
    
    email = forms.CharField(
        widget = forms.TextInput(
            attrs = {"style": "width: 50%;"},
        ),
        help_text = u"Optional. Override the User's email address",
        required=False,
    )
    
    organization = forms.CharField(
        widget = forms.TextInput(
            attrs = {"style": "width: 50%;"},
        ),
        help_text = u"Optional. Customers organization.",
        required=False,

    )
    
    save_api = forms.BooleanField(
        required = False,
        help_text = u"Checking this will save the customer to chargify",
    )
    
    
    class Meta:
        model = Customer
        
    def save(self, commit=True):        
        customer = super(CustomerAdminForm, self).save(commit=False)

        cd = self.cleaned_data
                
        customer.organization = ''
        
        if cd['first_name']:
            customer.first_name = cd['first_name']
        if cd['last_name']:
            customer.last_name = cd['last_name']
        if cd['organization']:
            customer.organization = cd['organization']
            
        if cd['save_api']:
            customer.save(save_api=True)
        else:
            customer.save()
            
        return customer
            
        

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'email', 'chargify_id', 'updated_at']
    
    fieldsets = (
        (None, {'fields': ('user', 'first_name', 'last_name', 'organization', 'save_api')}),
        
        #('Advanced', {
        #    'fields': ('chargify_created_at','chargify_updated_at','chargify_id',),
        #}),
    )
    
    form = CustomerAdminForm

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'handle', 'price', 'interval_unit', 'chargify_id']
    
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['product', 'get_state_display', 'customer', 'created_at', 'updated_at']
    list_filter = ['product', 'customer', 'state']

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CreditCard)
admin.site.register(Subscription, SubscriptionAdmin)
