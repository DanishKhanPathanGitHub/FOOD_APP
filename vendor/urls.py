from django.urls import path, include
from . import views
from accounts import views as AccountViews
urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendorDashboard'),
    path('profile/', views.profile, name='profile'),
    path('menu_manager/', views.menu_manager, name='menu_manager'),
    path('menu_manager/foodItem_by_category/<int:pk>', views.foodItem_by_category, name='foodItem_by_category'),
]

