from django import forms
from .models import Vendor
from accounts.utils import image_validator

class vendorForm(forms.ModelForm):
    vendor_license = forms.ImageField(widget=forms.FileInput(attrs={"class":"btn-btn-info"}), validators=[image_validator])
    class Meta:
        model = Vendor
        fields = ("vendor_name", "vendor_license",)
