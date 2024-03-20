from django.urls import path, include
from . import views
from accounts import views as AccountViews
urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendorDashboard'),
    path('profile/', views.profile, name='profile'),
    path('menu_manager/', views.menu_manager, name='menu_manager'),
    
    path('menu_manager/foodItem_by_category/<int:pk>', views.foodItem_by_category, name='foodItem_by_category'),
    
    path('menu_manager/category_add', views.category_add, name='category_add'),
    path('menu_manager/category_edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('menu_manager/category_delete/<int:pk>/', views.category_delete, name='category_delete'),

    path('menu_manager/food_add', views.food_add, name='food_add'),
    path('menu_manager/food_edit/<int:pk>/', views.food_edit, name='food_edit'),
    path('menu_manager/food_delete/<int:pk>/', views.food_delete, name='food_delete'),

    
]

