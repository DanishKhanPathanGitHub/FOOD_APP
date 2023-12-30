from django.shortcuts import render, redirect
from django.http import *
from .forms import *
from vendor.forms import vendorForm
from django.contrib import messages
# Create your views here.
def registerUser(request):
    user_form = userForm()
    if request.POST:
        user_form = userForm(request.POST)
        if user_form.is_valid():
            password = user_form.cleaned_data['password']
            user = user_form.save(commit=False)
            user.set_password(password)
            user.save()
            messages.success(request, "Your account has been registered succesfully")
            return redirect('registerUser')
        else:
            print('not valid')
    
    context ={
        "user_form": user_form
    }
    return render(request, 'accounts/registerUser.html', context)

def registerVendor(request):
    user_form = userForm()
    vendor_form = vendorForm()
    if request.POST:
        user_form = userForm(request.POST)
        vendor_form = vendorForm(request.POST, request.FILES)
        print(user_form.data, vendor_form.data)
        if user_form.is_valid() and vendor_form.is_valid():
            password = user_form.cleaned_data['password']
            user = user_form.save(commit=False)
            user.set_password(password)
            print("password set -->")
            user.role = 2
            print(f"user role set to {user.role}")
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            print("vendor user assign")
            vendor.vendor_profile = userProfile.objects.get(user=user)
            print('vendor user profile assign')
            vendor.save()
            print('vendor saved')
            messages.success(request, "Your account has been registered succesfully, Wait for approval")
            return redirect('registerVendor')
    context = {
        "user_form":user_form,
        "vendor_form": vendor_form,
    }
    return render(request, 'accounts/registerVendor.html', context)