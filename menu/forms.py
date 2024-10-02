# menu_app/forms.py

from django import forms

from .models import Menu, MenuItem, Category


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'description', 'logo', 'restaurant_name']


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'photo', 'price', 'description', 'categories', 'menus']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'menus']
