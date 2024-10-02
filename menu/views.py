# menu/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Menu, MenuItem, Category
from django.contrib.auth.decorators import login_required
from .forms import MenuForm, MenuItemForm, CategoryForm
from django.core.paginator import Paginator
from django.db.models import Q

def home(request):
    return render(request, 'menu/home.html')

@login_required
def menu_list(request):
    menus = Menu.objects.filter(user=request.user)
    return render(request, 'menu/menu_list.html', {'menus': menus})

@login_required
def menu_create(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.user = request.user
            menu.save()
            return redirect('menu_list')
    else:
        form = MenuForm()
    return render(request, 'menu/menu_form.html', {'form': form})

def menu_detail(request, slug):
    menu = get_object_or_404(Menu, slug=slug)
    categories = menu.categories.all()
    menu_items_without_category = menu.menu_items.filter(categories__isnull=True)
    context = {
        'menu': menu,
        'categories': categories,
        'menu_items_without_category': menu_items_without_category,
    }
    return render(request, 'menu/menu_detail.html', context)

@login_required
def menu_update(request, slug):
    menu = get_object_or_404(Menu, slug=slug, user=request.user)
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES, instance=menu)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuForm(instance=menu)
    return render(request, 'menu/menu_form.html', {'form': form})

@login_required
def menu_delete(request, slug):
    menu = get_object_or_404(Menu, slug=slug, user=request.user)
    if request.method == 'POST':
        menu.delete()
        return redirect('menu_list')
    return render(request, 'menu/menu_confirm_delete.html', {'menu': menu})

# Admin Dashboard
@login_required
def admin_dashboard(request):
    # Implement pagination and search
    query = request.GET.get('q', '')
    menu_items_list = MenuItem.objects.filter(user=request.user).filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ).order_by('name')

    paginator = Paginator(menu_items_list, 10)  # 10 items per page
    page_number = request.GET.get('page')
    menu_items = paginator.get_page(page_number)

    return render(request, 'menu/admin_dashboard.html', {'menu_items': menu_items, 'query': query})
