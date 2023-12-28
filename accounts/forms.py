from django import forms
from .models import *

class userForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ("firstname", "lastname", "username", "email", "phone_no", "password",)

    def clean(self):
        cleaned_data = super(userForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
