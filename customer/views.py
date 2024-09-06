from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import userProfile, User
from accounts.forms import userProfileForm, UserUpdateForm
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.utils import check_role_customer
from django.contrib import messages
# Create your views here.
@login_required(login_url='login')    
@user_passes_test(check_role_customer)
def customer_profile(request):
    user_profile = get_object_or_404(userProfile, user=request.user)
    if request.POST:
        user_profile_form = userProfileForm(request.POST, request.FILES, instance=user_profile)
        user_detail_form = UserUpdateForm(request.POST, instance=request.user)
        if user_profile_form.is_valid() and user_detail_form.is_valid():
            user_profile_form.save()
            user_detail_form.save()
            messages.success(request, 'Changes saved succesfully!')
            return redirect('customer_profile')
    else:
        user_profile_form = userProfileForm(instance=user_profile)
        user_detail_form = UserUpdateForm(instance=request.user)

    context = {
        "user_profile_form":user_profile_form,
        "user_profile":user_profile,
        "user_detail_form":user_detail_form,
    }
    return render(request, 'customer/customer_profile.html', context)