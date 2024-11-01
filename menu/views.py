from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from .constants import PAGINATION_PAGE_SIZE
from .forms import MenuForm, MenuItemForm, CategoryForm, MenuDetailForm
from .models import Menu, MenuItem, Category, MenuDetail
from .utils import get_s3_client


def home(request):
    if request.user.is_authenticated:
        return redirect('menu_list')
    return render(request, 'home.html')


@login_required
@require_http_methods(["GET"])
def menu_list(request):
    menus = Menu.objects.filter(user=request.user)
    return render(request, 'menu/menu_list.html', {'menus': menus})


@login_required
@require_http_methods(["PUT", "POST", "GET"])
def menu_create(request):
    if request.method == 'POST':
        menu_form = MenuForm(request.POST, request.FILES)
        menu_detail_form = MenuDetailForm(request.POST)

        if menu_form.is_valid() and menu_detail_form.is_valid():
            # Handle logo upload to S3 if provided
            logo = request.FILES.get('logo')
            logo_url = None
            if logo:
                logo_url = upload_logo(menu_form.instance.id, logo)

            # Save the Menu instance
            menu = menu_form.save(commit=False)
            menu.logo_url = logo_url
            menu.user = request.user
            menu.save()

            # Save the MenuDetail instance, linking it to the Menu
            menu_detail = menu_detail_form.save(commit=False)
            menu_detail.menu = menu
            menu_detail.save()

            return redirect('menu_list')
    else:
        menu_form = MenuForm()
        menu_detail_form = MenuDetailForm()

    is_update: bool = False
    return render(request, 'menu/menu_form.html', {
        'menu_form': menu_form,
        'menu_detail_form': menu_detail_form,
        'is_update': is_update
    })


@require_http_methods(["GET"])
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
@require_http_methods(["PUT", "POST", "GET"])
def menu_update(request, slug):
    menu = get_object_or_404(Menu, slug=slug, user=request.user)

    try:
        menu_detail = MenuDetail.objects.get(menu=menu)
    except MenuDetail.DoesNotExist:
        menu_detail = MenuDetail(menu=menu)
        menu_detail.save()

    if request.method == 'POST':
        menu_form = MenuForm(request.POST, request.FILES, instance=menu)
        menu_detail_form = MenuDetailForm(request.POST, instance=menu_detail)

        if menu_form.is_valid() and menu_detail_form.is_valid():
            # Handle logo upload replacement
            logo = request.FILES.get('logo')

            if logo:
                logo_url = upload_logo(menu.id, logo)
                menu.logo_url = logo_url

            # Save the updated Menu
            menu_form.save()

            # Save the updated MenuDetail
            menu_detail_form.save()

            return redirect('menu_list')
    else:
        menu_form = MenuForm(instance=menu)
        menu_detail_form = MenuDetailForm(instance=menu_detail)

    is_update: bool = True
    return render(request, 'menu/menu_form.html', {
        'menu_form': menu_form,
        'menu_detail_form': menu_detail_form,
        'is_update': is_update
    })


@login_required
@require_http_methods(["POST", "GET"])
def menu_delete(request, slug):
    menu = get_object_or_404(Menu, slug=slug, user=request.user)
    if request.method == 'POST':
        menu.delete()
        return redirect('menu_list')
    return render(request, 'menu/menu_confirm_delete.html', {'menu': menu})


# Admin Dashboard
@login_required
@require_http_methods(["GET"])
def admin_dashboard(request):
    # Implement pagination and search
    query = request.GET.get('q', '')
    menu_items_list = MenuItem.objects.filter(user=request.user).filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ).order_by('name')

    paginator = Paginator(menu_items_list, 10)  # 10 items per page
    page_number = request.GET.get('page')
    menu_items = paginator.get_page(page_number)

    return render(request, 'admin_dashboard.html', {'menu_items': menu_items, 'query': query})


@login_required
@require_http_methods(["GET"])
def menu_item_list(request, slug):
    menu = get_object_or_404(Menu, slug=slug, user=request.user)
    menu_items = menu.menu_items.all()

    # Add pagination
    paginator = Paginator(menu_items, PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'menu/menu_item/menu_item_list.html', {
        'menu': menu,
        'page_obj': page_obj
    })


@login_required
@require_http_methods(["POST", "GET"])
def menu_item_create(request, slug):
    menu = get_object_or_404(Menu, slug=slug, user=request.user)
    category_id = request.GET.get('category')
    initial_data = {}
    category = None
    if category_id:
        try:
            category = Category.objects.get(id=category_id, menus=menu)
            initial_data['categories'] = [category]
        except Category.DoesNotExist:
            pass
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, menu=menu)
        if form.is_valid():

            # Upload photo to S3
            photo = request.FILES.get('photo')
            photo_url = None
            if photo:
                photo_url = upload_photo(menu.id, form.instance.id, photo)

            menu_item = form.save(commit=False)
            menu_item.image_url = photo_url
            menu_item.save()
            menu_item.menus.add(menu)

            if category:
                menu_item.categories.add(category)
                menu_item.save()

            return redirect('menu_item_list', slug=menu.slug)
    else:
        form = MenuItemForm(menu=menu, initial=initial_data)
    is_update: bool = False
    return render(request, 'menu/menu_item/menu_item_form.html',
                  {'form': form, 'menu': menu, 'is_update': is_update})


@login_required
@require_http_methods(["GET"])
def menu_item_detail(request, slug, menu_item_id):
    menu = get_object_or_404(Menu, slug=slug, user=request.user)
    menu_item = get_object_or_404(MenuItem, id=menu_item_id, menus=menu)
    return render(request, 'menu/menu_item/menu_item_detail.html', {'menu': menu, 'menu_item': menu_item})


@login_required
@require_http_methods(["PUT", "POST", "GET"])
def menu_item_update(request, slug, menu_item_id):
    menu = get_object_or_404(Menu, slug=slug, user=request.user)
    menu_item = get_object_or_404(MenuItem, id=menu_item_id, menus=menu)

    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=menu_item, menu=menu)

        if form.is_valid():
            # Check if "Remove Category" flag is set
            if request.POST.get('remove_category') == 'true':
                menu_item.categories.clear()

            # Check if a new photo is uploaded
            photo = request.FILES.get('photo')
            if photo:
                # Update the photo in S3 and get the new URL
                photo_url = upload_photo(menu.id, menu_item.id, photo)
                menu_item.image_url = photo_url

            form.save()
            return redirect('menu_item_list', slug=menu.slug)
    else:
        form = MenuItemForm(instance=menu_item, menu=menu)

    is_update: bool = True
    return render(request, 'menu/menu_item/menu_item_form.html', {
        'form': form,
        'menu': menu,
        'menu_item': menu_item,
        'is_update': is_update
    })


@login_required
@require_http_methods(["DELETE", "POST", "GET"])
def menu_item_delete(request, slug, menu_item_id):
    menu = get_object_or_404(Menu, slug=slug, user=request.user)
    menu_item = get_object_or_404(MenuItem, id=menu_item_id, menus=menu)
    if request.method == 'POST':
        # Remove the MenuItem from the Menu
        menu_item.menus.remove(menu)
        # If the MenuItem is not associated with any other Menus, delete it
        if menu_item.menus.count() == 0:
            menu_item.delete()
        return redirect('menu_item_list', slug=menu.slug)
    return render(request, 'menu/menu_item/menu_item_confirm_delete.html', {'menu': menu, 'menu_item': menu_item})


@login_required
@require_http_methods(["GET"])
def category_list(request, slug):
    menu = get_object_or_404(Menu, slug=slug, user=request.user)
    categories = menu.categories.all()
    return render(request, 'menu/category/category_list.html', {'menu': menu, 'categories': categories})


@login_required
@require_http_methods(["POST", "GET"])
def category_create(request, slug):
    menu = get_object_or_404(Menu, slug=slug, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            # Associate the Category with the Menu
            category.menus.add(menu)
            return redirect('category_list', slug=menu.slug)
    else:
        form = CategoryForm()
    return render(request, 'menu/category/category_form.html', {'form': form, 'menu': menu})


@login_required
@require_http_methods(["GET"])
def category_detail(request, slug, category_id):
    menu = get_object_or_404(Menu, slug=slug, user=request.user)
    category = get_object_or_404(Category, id=category_id, menus=menu)
    # Get MenuItems in this Category and associated with the Menu
    menu_items = category.menu_items.filter(menus=menu)
    return render(request, 'menu/category/category_detail.html', {'menu': menu, 'category': category, 'menu_items': menu_items})


@login_required
@require_http_methods(["PUT", "POST", "GET"])
def category_update(request, slug, category_id):
    menu = get_object_or_404(Menu, slug=slug, user=request.user)
    category = get_object_or_404(Category, id=category_id, menus=menu)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list', slug=menu.slug)
    else:
        form = CategoryForm(instance=category)

    is_update: bool = True
    return render(request, 'menu/category/category_form.html', {'form': form, 'menu': menu, 'is_update': is_update})


@login_required
@require_http_methods(["DELETE", "POST", "GET"])
def category_delete(request, slug, category_id):
    menu = get_object_or_404(Menu, slug=slug, user=request.user)
    category = get_object_or_404(Category, id=category_id, menus=menu)
    if request.method == 'POST':
        # Remove the Category from the Menu
        category.menus.remove(menu)
        # If the Category is not associated with any other Menus, delete it
        if category.menus.count() == 0:
            category.delete()
        return redirect('category_list', slug=menu.slug)
    return render(request, 'menu/category/category_confirm_delete.html', {'menu': menu, 'category': category})


def upload_photo(menu_id: str, menu_item_id: str, image_file: bytes):
    object_name = f"menus/{menu_id}/menu_items/{menu_item_id}/photo.jpg"
    s3_client = get_s3_client()

    # Upload image to S3 using the presigned URL
    s3_client.put_object(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=object_name,
        Body=image_file.read(),
        ContentType=image_file.content_type
    )

    # Save the Dish object with the S3 URL
    return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{object_name}"


def upload_logo(menu_id: str, image_file: bytes):
    object_name = f"menus/{menu_id}/logo.jpg"
    s3_client = get_s3_client()

    # Upload image to S3 using the presigned URL
    s3_client.put_object(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=object_name,
        Body=image_file.read(),
        ContentType=image_file.content_type
    )

    # Return the S3 URL of the uploaded logo
    return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{object_name}"
