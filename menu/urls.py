# menu_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menus/', views.menu_list, name='menu_list'),
    path('menus/create/', views.menu_create, name='menu_create'),
    path('menus/<slug:slug>/', views.menu_detail, name='menu_detail'),
    path('menus/<slug:slug>/update/', views.menu_update, name='menu_update'),
    path('menus/<slug:slug>/delete/', views.menu_delete, name='menu_delete'),
    # Similar URLs for MenuItems and Categories
    # path('menu-items/', views.menu_item_list, name='menu_item_list'),
    # path('menu-items/create/', views.menu_item_create, name='menu_item_create'),
    # path('menu-items/<slug:slug>/', views.menu_item_detail, name='menu_item_detail'),
    # path('menu-items/<slug:slug>/update/', views.menu_item_update, name='menu_item_update'),
    # path('menu-items/<slug:slug>/delete/', views.menu_item_delete, name='menu_item_delete'),
    # path('categories/', views.category_list, name='category_list'),
    # path('categories/create/', views.category_create, name='category_create'),
    # path('categories/<slug:slug>/', views.category_detail, name='category_detail'),
    # path('categories/<slug:slug>/update/', views.category_update, name='category_update'),
    # path('categories/<slug:slug>/delete/', views.category_delete, name='category_delete'),

    # Admin area
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
