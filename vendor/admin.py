from django.contrib import admin
from .models import Vendor
# Register your models here.
@admin.register(Vendor)
class vendorAadmin(admin.ModelAdmin):
    list_display = ('user', 'vendor_name', 'created_at', 'is_approved',)


