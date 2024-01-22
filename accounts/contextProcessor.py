from vendor.models import Vendor

def get_vednor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor=None
    return dict(vendor=vendor)