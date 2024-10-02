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
    path('menus/<slug:slug>/menu-items/', views.menu_item_list, name='menu_item_list'),
    path('menus/<slug:slug>/menu-items/create/', views.menu_item_create, name='menu_item_create'),
    path('menus/<slug:slug>/menu-items/<str:menu_id>/', views.menu_item_detail, name='menu_item_detail'),
    path('menus/<slug:slug>/menu-items/<str:menu_id>/update/', views.menu_item_update, name='menu_item_update'),
    path('menus/<slug:slug>/menu-items/<str:menu_id>/delete/', views.menu_item_delete, name='menu_item_delete'),
    path('menus/<slug:slug>/categories/', views.category_list, name='category_list'),
    path('menus/<slug:slug>/categories/create/', views.category_create, name='category_create'),
    path('menus/<slug:slug>/categories/<str:category_id>/', views.category_detail, name='category_detail'),
    path('menus/<slug:slug>/categories/<str:category_id>/update/', views.category_update, name='category_update'),
    path('menus/<slug:slug>/categories/<str:category_id>/delete/', views.category_delete, name='category_delete'),

    # Admin area
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
