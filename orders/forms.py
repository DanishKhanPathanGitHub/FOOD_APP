from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields = [
            'firstname', 'lastname', 'phone_no', 
            'email', 'address', 'country', 'state', 'city', 'pincode'
        ]
        