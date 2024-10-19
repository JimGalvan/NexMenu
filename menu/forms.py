# menu_app/forms.py

from django import forms

from .models import Menu, Locations, CuisineType, DietaryOption, Tag
from .models import MenuItem, Category


# menu/forms.py

class MenuForm(forms.ModelForm):
    average_rating = forms.FloatField(widget=forms.HiddenInput(), required=False)
    operating_hours = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    locations = forms.ModelMultipleChoiceField(queryset=Locations.objects.all(), required=False)
    cuisine_type = forms.ModelMultipleChoiceField(queryset=CuisineType.objects.all(), required=False)
    dietary_options = forms.ModelMultipleChoiceField(queryset=DietaryOption.objects.all(), required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
    delivery_options = forms.ChoiceField(choices=[
        ('pickup', 'Pickup'),
        ('delivery', 'Delivery'),
        ('both', 'Both'),
        ('none', 'None')
    ], required=False)

    class Meta:
        model = Menu
        fields = ['name', 'description', 'logo', 'restaurant_name', 'average_rating', 'operating_hours', 'locations',
                  'cuisine_type', 'dietary_options', 'tags', 'delivery_options']
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
