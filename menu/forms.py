# menu_app/forms.py

from django import forms

from .models import Menu, MenuItem, Category


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'description', 'logo', 'restaurant_name']
        widgets = {
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'photo', 'price', 'description', 'categories']

    def __init__(self, *args, **kwargs):
        menu = kwargs.pop('menu', None)
        super(MenuItemForm, self).__init__(*args, **kwargs)
        if menu:
            # Limit the categories to those associated with the current menu
            self.fields['categories'].queryset = menu.categories.all()


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
