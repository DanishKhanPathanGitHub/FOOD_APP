from django.shortcuts import render, redirect
from django.http import *
from .forms import *
from vendor.forms import vendorForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
# Create your views here.

#forbiding customer to access the vendor dashboard
def check_role_vendor(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
    
#forbiding vendor to access the customer dashboard
def check_role_customer(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'you are already logged in')
        return redirect('myAccount')
    else:
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
    if request.user.is_authenticated:
        messages.warning(request, 'you are already logged in')
        return redirect('myAccount')
    else:
        user_form = userForm()
        vendor_form = vendorForm()
        if request.POST:
            user_form = userForm(request.POST)
            vendor_form = vendorForm(request.POST, request.FILES)
            #print(user_form.data, vendor_form.data)
            if user_form.is_valid() and vendor_form.is_valid():
                password = user_form.cleaned_data['password']
                user = user_form.save(commit=False)
                user.set_password(password)
                #print("password set -->")
                user.role = 2
                #print(f"user role set to {user.role}")
                user.save()
                vendor = vendor_form.save(commit=False)
                vendor.user = user
                #print("vendor user assign")
                vendor.vendor_profile = userProfile.objects.get(user=user)
                #print('vendor user profile assign')
                vendor.save()
                #print('vendor saved')
                messages.success(request, "Your account has been registered succesfully, Wait for approval")
                return redirect('registerVendor')
        context = {
            "user_form":user_form,
            "vendor_form": vendor_form,
        }
        return render(request, 'accounts/registerVendor.html', context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'you are already logged in')
        return redirect('myAccount')
    else:
        if request.POST:
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(email=email, password=password)

            if user is not None:
                auth.login(request, user)
                messages.success(request, "You are now logged in")
                return redirect('myAccount')
            else:
                messages.error(request, 'invalid login credentials')
                return redirect('login')
            
        return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.info(request, 'you are logged out')
    return redirect('login')
    
@login_required(login_url='login')    
def myAccount(request):
    redirecturl = '/'
    user = request.user
    if user.role == 1:
        redirecturl = 'custDashboard'
    elif user.role == 2:
        redirecturl = 'vendorDashboard'
    elif user.role and user.is_active == True:
        redirecturl = 'admin/'
    
    return redirect(redirecturl)

@login_required(login_url='login')    
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    context = {}
    return render(request, 'accounts/vendorDashboard.html', context)

@login_required(login_url='login') 
@user_passes_test(check_role_customer)   
def custDashboard(request):
    context = {}
    return render(request, 'accounts/custDashboard.html', context)