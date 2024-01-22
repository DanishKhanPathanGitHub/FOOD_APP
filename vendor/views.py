from django.shortcuts import render

# Create your views here.
def profile(request):
    context = {}
    return render(request, 'vendor/vendorProfile.html', context)
