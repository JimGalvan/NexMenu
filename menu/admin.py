# menu_app/admin.py

from django.contrib import admin
from django.utils.html import format_html

from .models import Menu, MenuItem, Category

admin.site.register(MenuItem)
admin.site.register(Category)


class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant_name', 'logo_thumbnail')

    def logo_thumbnail(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" />', obj.logo.url)
        else:
            return "No Logo"

    logo_thumbnail.short_description = 'Logo'


admin.site.register(Menu, MenuAdmin)
