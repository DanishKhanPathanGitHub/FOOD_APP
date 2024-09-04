from accounts.forms import userProfileForm
from accounts.models import userProfile
from .forms import vendorForm, openingHoursForm
from .models import *
from menu.models import foodCategory, foodItem
from menu.forms import foodCategoryForm, foodItemForm

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse

from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor


# Create your views here.
@login_required(login_url='login')    
@user_passes_test(check_role_vendor)
def profile(request):
    user_profile = get_object_or_404(userProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.POST:
        user_profile_form = userProfileForm(request.POST, request.FILES, instance=user_profile)
        vendor_form = vendorForm(request.POST, request.FILES, instance=vendor)
        if user_profile_form.is_valid() and vendor_form.is_valid():
            user_profile_form.save()
            vendor_form.save()
            messages.success(request, 'Changes saved succesfully!')
            return redirect('profile')
    else:
        user_profile_form = userProfileForm(instance=user_profile)
        vendor_form = vendorForm(instance=vendor)

    context = {
        "user_profile_form":user_profile_form,
        "vendor_form":vendor_form,
        "user_profile":user_profile,
    }
    return render(request, 'vendor/vendorProfile.html', context)

@login_required(login_url='login')    
@user_passes_test(check_role_vendor)
def menu_manager(request):
    vendor = Vendor.objects.get(user=request.user)
    categories = foodCategory.objects.filter(vendor=vendor)
    context ={
        "categories":categories,
    }
    return render(request, 'vendor/menu.html', context)

@login_required(login_url='login')    
@user_passes_test(check_role_vendor)
def foodItem_by_category(request, pk=None):
    vendor = Vendor.objects.get(user=request.user)
    category = get_object_or_404(foodCategory, pk=pk)
    food_items = foodItem.objects.filter(vendor=vendor, category=category).order_by('created_at')
    context = {
        "category":category,
        "food_items":food_items,
    }
    return render(request, 'vendor/foodItem_by_category.html', context)

@login_required(login_url='login')    
@user_passes_test(check_role_vendor)
def category_add(request):
    if request.POST:
        #print("request is post")
        category_form = foodCategoryForm(request.POST)
        if category_form.is_valid():
            category = category_form.save(commit=False)
            category.vendor = Vendor.objects.get(user=request.user)
            category_form.save()
            messages.success(request, "category added succesfully")
            return  redirect('menu_manager')
        else:
            print("form is not valid")
            print(category_form.fields)
            print(category_form.errors)
    else: 
        category_form = foodCategoryForm()
        
    context = {
        "category_form":category_form,
    }
    return render(request, 'vendor/category_add.html', context)

@login_required(login_url='login')    
@user_passes_test(check_role_vendor)
def category_edit(request, pk=None):
    category = get_object_or_404(foodCategory, pk=pk)
    if request.POST:
        category_form = foodCategoryForm(request.POST, instance=category)
        if category_form.is_valid():
            category = category_form.save(commit=False)
            category.vendor = Vendor.objects.get(user=request.user)
            category_form.save()
            messages.success(request, "category updated succesfully")
            return  redirect('menu_manager')
        else:
            print("form is not valid")
            print(category_form.fields)
            print(category_form.errors)
    else: 
        category_form = foodCategoryForm(instance=category)
        
    context = {
        "category":category,
        "category_form":category_form,
    }
    return render(request, 'vendor/category_edit.html', context)

@login_required(login_url='login')    
@user_passes_test(check_role_vendor)
def category_delete(request, pk=None):
    category = get_object_or_404(foodCategory, pk=pk)
    category.delete()
    messages.success(request, "category has been deleted succesfully")
    return  redirect('menu_manager')



@login_required(login_url='login')    
@user_passes_test(check_role_vendor)
def food_add(request):
    vendor = Vendor.objects.get(user=request.user)
    food_item_form = foodItemForm(vendor_id=vendor.id)
    if request.POST:
        food_item_form = foodItemForm(request.POST, request.FILES, vendor_id=vendor.id)
        if food_item_form.is_valid():
            food_item = food_item_form.save(commit=False)
            food_item.vendor = Vendor.objects.get(user=request.user)
            food_item_form.save()
            messages.success(request, "food item added succesfully")
            return  redirect('foodItem_by_category', food_item.category.id)
        else:
            print("form is not valid")
            print(food_item_form.errors)
        
    context = {
        "food_item_form":food_item_form,
    }
    return render(request, 'vendor/food_add.html', context)       
    
@login_required(login_url='login')    
@user_passes_test(check_role_vendor)
def food_edit(request, pk=None):
    food = get_object_or_404(foodItem, pk=pk)
    vendor = Vendor.objects.get(user=request.user)
    if request.POST:
        food_item_form = foodItemForm(request.POST, request.FILES, instance=food, vendor_id=vendor.id)
        if food_item_form.is_valid():
            food_item = food_item_form.save(commit=False)
            food_item.vendor = Vendor.objects.get(user=request.user)
            food_item_form.save()
            messages.success(request, "food updated succesfully")
            return  redirect('foodItem_by_category', food_item.category.id)
        else:
            print("form is not valid")
            print(food_item_form.fields)
            print(food_item_form.errors)
            
    else: 
        food_item_form = foodItemForm(instance=food, vendor_id=vendor.id)
        
    context = {
        "food":food,
        "food_item_form":food_item_form,
    }
    return render(request, 'vendor/food_edit.html', context)

@login_required(login_url='login')    
@user_passes_test(check_role_vendor)
def food_delete(request, pk=None):
    food = get_object_or_404(foodItem, pk=pk)
    category = food.category
    food.delete()
    messages.success(request, "food has been deleted succesfully")
    return  redirect('foodItem_by_category', category.id)


@login_required(login_url='login')    
@user_passes_test(check_role_vendor)
def opening_hours(request):
    opening_hours = OpeningHours.objects.filter(vendor=Vendor.objects.get(user=request.user))
    form = openingHoursForm()
    context = {
        "opening_hours":opening_hours,
        "form":form,
    }
    return render(request, 'vendor/opening_hours.html', context)

@user_passes_test(check_role_vendor)
def opening_hours_add(request):
    if request.user.is_authenticated:
        vendor = Vendor.objects.get(user=request.user)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.POST:
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')=='true'

            try:
                hour = OpeningHours.objects.create(vendor=vendor, day=day, from_hour=from_hour, to_hour=to_hour, is_closed=is_closed)
                if hour:
                    object = OpeningHours.objects.get(id=hour.id)
                    if object.is_closed:
                        response = {
                            'status':'success', 'id':object.id, 
                            'day':object.get_day_display(), 
                            'is_closed':'Closed'
                        }
                    else:
                        response = {
                            'status':'success', 'id':object.id, 
                            'day':object.get_day_display(), 
                            'from_hour':object.from_hour, 'to_hour':object.to_hour
                        }
                return JsonResponse(response)
            
            except Exception as e:
                try:
                    existing_day = OpeningHours.objects.get(vendor=vendor, day=day)
                    message = f'entry for the {existing_day.get_day_display()} already exist'
                except:
                    existing_day = None
                    message = f'Invalid entry'
                response = {
                    'status':'Entry updated for', 
                    'message':message,
                }
                return JsonResponse(response)
        else:
            return HttpResponse("Invalid request")
        

@user_passes_test(check_role_vendor)
def opening_hours_delete(request, hour_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                hour = OpeningHours.objects.get(id=hour_id)
                if hour:
                    name = hour.get_day_display()
                    hour.delete()   
                    return JsonResponse({
                        'status':'success',
                        'message':f'entry for {name} deleted', 
                    })   
            except:
                return JsonResponse({'status':'Failed', 'message':'This entry does not exist'})
        else:
            return JsonResponse({'status':'Failed', 'message':'invalid request'})