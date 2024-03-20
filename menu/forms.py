from django import forms
from .models import *
from accounts.utils import image_validator

class foodCategoryForm(forms.ModelForm):
    class Meta:
        model = foodCategory
        fields = ["category_name", "description",]
        

class foodItemForm(forms.ModelForm):
    image=forms.ImageField(widget=forms.FileInput(attrs={"class":"btn-btn-info"}), validators=[image_validator])
    class Meta:
        model = foodItem
        fields = ["image", "food_name", "category", "description", "price", "is_available",]
