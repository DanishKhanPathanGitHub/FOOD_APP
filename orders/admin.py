from django.contrib import admin
from .models import *
# Register your models here.

class orderFoodInline(admin.TabularInline):
    model = OrderedFood
    readonly_fields = ('order', 'payment', 'user', 'fooditem', 'quantity', 'price', 'amount')
    extra = 0

class orderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'name', 'phone_no', 'email', 'total',
        'payment_method', 'status', 'is_ordered'
    ]
    inlines = [orderFoodInline]

admin.site.register(Payment)
admin.site.register(Order, orderAdmin)
admin.site.register(OrderedFood)
