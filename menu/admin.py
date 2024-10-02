# menu_app/admin.py

from django.contrib import admin
from .models import Menu, MenuItem, Category

admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(Category)
