from django.db import models
from accounts.models import User, userProfile
from menu.models import foodItem

# Create your models here.
class Payment(models.Model):
    PAYMENT_METHOD = (
        ('RazorPay', 'RazorPay'),
        ('PayPal', 'PayPal'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=50)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.transaction_id
    
class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=25)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=10, blank=True)
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=25, blank=True)
    state = models.CharField(max_length=25, blank=True)
    city = models.CharField(max_length=30)
    pincode = models.CharField(max_length=12)
    total = models.FloatField()
    tax_data = models.JSONField(blank=True, help_text="Data format: {'tax_type':{'tax_percentage':'tax_amount'}}")
    total_tax = models.FloatField()
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def name(self):
        return f'{self.firstname} {self.lastname}'
    
    def __str__(self):
        return self.order_number
    
class OrderedFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(foodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fooditem.food_name
    
    
    