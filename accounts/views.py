from django.shortcuts import render, redirect
from django.http import *
from .forms import *
from django.contrib import messages
# Create your views here.
def registerUser(request):
    userform = userForm()
    if request.POST:
        userform = userForm(request.POST)
        if userform.is_valid():
            password = userform.cleaned_data['password']
            user = userform.save(commit=False)
            user.set_password(password)
            user.save()
            messages.success(request, "Your account has been registered succesfully")
            return redirect('registerUser')
        else:
            print('not valid')
    
    context ={
        "user_form": userform
    }
    return render(request, 'accounts/registerUser.html', context)
