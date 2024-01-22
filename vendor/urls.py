from django.urls import path, include
from . import views
from accounts import views as AccountViews
urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendorDashboard'),
    path('profile/', views.profile, name='profile')

]

