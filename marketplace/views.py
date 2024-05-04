from django.shortcuts import render, get_object_or_404
from vendor.models import Vendor
from menu.models import foodCategory, foodItem
from django.db.models import Prefetch
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
    context = {
        "vendor": vendor,
        "categories":categories,
    }
    return render(request, 'marketplace/vendor_detail.html', context)