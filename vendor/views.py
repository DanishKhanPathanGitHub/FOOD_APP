from django.shortcuts import render, get_object_or_404, redirect
from accounts.forms import userProfileForm
from accounts.models import userProfile
from .forms import vendorForm
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
# Create your views here.
@login_required(login_url='login')    
@user_passes_test(check_role_vendor)
def profile(request):

    user_profile = get_object_or_404(userProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.POST:
        print('request is post')
        user_profile_form = userProfileForm(request.POST, request.FILES, instance=user_profile)
        vendor_form = vendorForm(request.POST, request.FILES, instance=vendor)
        print(user_profile_form.fields)
        if user_profile_form.is_valid() and vendor_form.is_valid():
            user_profile_form.save()
            vendor_form.save()
            messages.success(request, 'Changes saved succesfully!')
            return redirect('profile')
    else:
        print('request is get')
        user_profile_form = userProfileForm(instance=user_profile)
        vendor_form = vendorForm(instance=vendor)

    context = {
        "user_profile_form":user_profile_form,
        "vendor_form":vendor_form,
        "user_profile":user_profile,
        "vendor":vendor,
    }
    return render(request, 'vendor/vendorProfile.html', context)
