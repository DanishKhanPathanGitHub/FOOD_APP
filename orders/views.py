from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.utils import check_role_customer
from marketplace.contextProcessor import get_cart_counter,  get_cart_total
from datetime import datetime
import simplejson

from marketplace.models import Cart
from .models import Order, OrderedFood, Payment
from .forms import OrderForm
from menu.models import foodItem
from accounts.models import User
from accounts.utils import send_notification

import razorpay
from food.settings import RZP_KEY_ID, RZP_KEY_SECRET
# Create your views here.

client = razorpay.Client(auth=(RZP_KEY_ID, RZP_KEY_SECRET))

@user_passes_test(check_role_customer)
@login_required(login_url='login')
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    if get_cart_counter(request)["cart_count"] < 1:
        return redirect('marketplace')
    
    subtotal = get_cart_total(request)['subtotal']
    taxtotal = get_cart_total(request)['taxtotal']
    total = get_cart_total(request)['total']
    taxdata = get_cart_total(request)['taxes']

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user
            order.total = total
            order.total_tax = taxtotal
            order.tax_data = simplejson.dumps(taxdata)
            order.payment_method = request.POST['payment_method']
            order.save()
            order.order_number = datetime.now().strftime('%Y%m%d%H%M%S') + str(order.id)
            order.save()

            DATA = {
                "amount": float(order.total)*100,
                "currency": "INR",
                "receipt": "receipt #"+order.order_number,
                "notes": {
                    "key1": "value3",
                    "key2": "value2"
                }
            }
            rzp_order = client.order.create(data=DATA)
            rzp_order_id = rzp_order['id']
            context = {
                'order':order,
                'rzp_order_id':rzp_order_id,
                'cart_items':cart_items,
                'RZP_KEY_ID':RZP_KEY_ID,
                'rzp_amount':float(order.total)*100,
            }
            return render(request, 'orders/place_order.html', context)
    return render(request, 'orders/place_order.html')


@user_passes_test(check_role_customer)
@login_required(login_url='login')
def payments(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')
        order = Order.objects.get(user=request.user, order_number=order_number)
        
        #generating payment object
        payment = Payment.objects.create(
            user = request.user,
            transaction_id = transaction_id,
            payment_method = payment_method,
            amount  = order.total,
            status = status
        )
        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()
        
        #moving cart items to ordered food 
        
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_food = OrderedFood.objects.create(
                order = order,
                payment = payment,
                user = request.user,
                fooditem = item.fooditem,
                quantity = item.quantity,
                price =  item.fooditem.price,
                amount =  item.fooditem.price*item.quantity
            )
            ordered_food.save()
        
        #sending confirmation email to customer
        send_notification(
            mail_subject="Your order confirmed!",
            email_template="orders/order_confirmation_email.html",
            context={
                'order':order,
                'user':request.user,
            },
            to_emails= [order.email]
        )
    
        #sending confirmation email to vendor
        emails = set()
        for item in cart_items:
            emails.add(item.fooditem.vendor.user.email)
        send_notification(
            mail_subject="You have received new order!",
            email_template="orders/order_received_email.html",
            context={
                'order':order,
            },
            to_emails= list(emails)
        )

        #clearing the cart
        """
        cart_items.delete()
        """
        response = {
            'order_number':order_number,
            'transaction_id':transaction_id,
        }
        return JsonResponse(response)
    return HttpResponse


@user_passes_test(check_role_customer)
@login_required(login_url='login')
def order_complete(request):
    order_number = request.GET.get('order_no')
    transaction_id = request.GET.get('trans_id')
    print(order_number, transaction_id)
    try:
        print("inside try block")
        order = Order.objects.get(order_number=order_number, payment__transaction_id=transaction_id, is_ordered=True)
        print("order created: ", order.name)
        ordered_food = OrderedFood.objects.filter(order=order)
        tax_data = simplejson.loads(order.tax_data)
        print("json loaded")
        subtotal = 0
        for item in ordered_food:
            subtotal+= item.fooditem.price * item.quantity 
        context = {
            'order':order,
            'ordered_food':ordered_food,
            'tax_data':tax_data,
            'subtotal':subtotal,
        }
        return redirect('order_detail', order.order_number)
    except:
        print("inside except")
        return redirect('home')
    