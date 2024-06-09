from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, JsonResponse
from vendor.models import Vendor
from menu.models import foodCategory, foodItem
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from .models import Cart
from .contextProcessor import get_cart_counter, get_cart_total
# Create your views here.


def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendors_count = vendors.count()
    context = {
        "vendors":vendors,
        "vendors_count": vendors_count,
    }
    return render(request, 'marketplace/listings.html', context)


def vendor_detail(request, slug):
    vendor = get_object_or_404(Vendor, slug=slug)
    categories = foodCategory.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset = foodItem.objects.filter(is_available=True)
        )
    )

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        "vendor": vendor,
        "categories":categories,
        "cart_items":cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)

def add_to_cart(request, food_id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                food_item = foodItem.objects.get(id=food_id)
                #check if user had already added food in cart
                try:
                    food_item_cart = Cart.objects.get(user=request.user, fooditem=food_item)
                    food_item_cart.quantity += 1
                    food_item_cart.save()
                    return JsonResponse(
                        {
                            'status':'success',
                            'message': 'quantity increased by one', 
                            'cart_counter':get_cart_counter(request), 
                            'qty':food_item_cart.quantity,
                            'get_cart_total':get_cart_total(request),
                        }
                    )
                except:
                    food_item_cart = Cart.objects.create(user=request.user, fooditem=food_item, quantity=1)
                    return JsonResponse(
                        {
                            'status':'success', 
                            'message':'food added to the cart', 
                            'cart_counter':get_cart_counter(request), 
                            'qty':food_item_cart.quantity,
                            'get_cart_total':get_cart_total(request),
                        }
                    )
                    
            except:
                return JsonResponse(
                    {
                        'status':'Failed', 
                        'message':'This food does not exist'
                    }
                )
        else:
            return JsonResponse(
                {
                    'status':'Failed', 
                    'message':'Invalid request'
                }
            )       
    else:
        return JsonResponse(
            {
                'status':'login_required',
                'message':'Please login to continue'
            }
        )

def decrease_cart(request, food_id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                food_item = foodItem.objects.get(id=food_id)
                #check if user had already added food in cart
                try:
                    food_item_cart = Cart.objects.get(user=request.user, fooditem=food_item)
                    if food_item_cart.quantity > 1:
                        food_item_cart.quantity -= 1 
                        food_item_cart.save()
                    else:
                        food_item_cart.delete()
                        food_item_cart.quantity = 0
                    return JsonResponse({'status':'success', 'cart_counter':get_cart_counter(request), 'qty':food_item_cart.quantity, 'get_cart_total':get_cart_total(request)})
                except:
                    return JsonResponse({'status':'Failed', 'message':'You do not have this item in your cart'})
                    
            except:
                return JsonResponse({'status':'Failed', 'message':'This food does not exist'})
        else:
            return JsonResponse({'status':'Failed', 'message':'Invalid request'})
    else:
        return JsonResponse({'status':'login_required', 'message':'login to continue'})    
    
@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        "cart_items":cart_items,
    }
    return render(request, 'marketplace/cart.html', context)

def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()   
                    return JsonResponse({'status':'success', 'message':'cart item deleted', 'cart_counter':get_cart_counter(request),'get_cart_total':get_cart_total(request)})   
            except:
                return JsonResponse({'status':'Failed', 'message':'cart item does not exist'})
        else:
            return JsonResponse({'status':'Failed', 'message':'invalid request'})
        
