from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render

from menu.models import Menu, CuisineType


def index(request):
    menus_list = Menu.objects.filter(show_on_catalog=True)

    # Handle Search
    search_query = request.GET.get('search', '')
    if search_query:
        menus_list = menus_list.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(restaurant_name__icontains=search_query)
        )

    # Handle Filters
    category_filter = request.GET.get('category', '')
    if category_filter:
        menus_list = menus_list.filter(detail__cuisine_type__name__icontains=category_filter)
    elif category_filter == 'all':
        menus_list = menus_list.all()

    cuisine_filter = request.GET.get('cuisine', '')
    if cuisine_filter:
        menus_list = menus_list.filter(detail__cuisine_type__name__icontains=cuisine_filter)

    dietary_filter = request.GET.get('dietary', '')
    if dietary_filter:
        menus_list = menus_list.filter(detail__dietary_options__name__icontains=dietary_filter)

    delivery_filter = request.GET.get('delivery', '')
    if delivery_filter:
        if delivery_filter:
            if delivery_filter == 'both':
                menus_list = menus_list.filter(detail__delivery_options__in=['both'])
            elif delivery_filter == 'pickup':
                menus_list = menus_list.filter(detail__delivery_options__in=['pickup', 'both'])
            elif delivery_filter == 'delivery':
                menus_list = menus_list.filter(detail__delivery_options__in=['delivery', 'both'])
            elif delivery_filter == 'none':
                menus_list = menus_list.exclude(detail__delivery_options__in=['pickup', 'delivery'])
            else:
                menus_list = menus_list.filter(detail__delivery_options__icontains=delivery_filter)

    # Handle Sorting
    sort_option = request.GET.get('sort', '')
    if sort_option == 'name_asc':
        menus_list = menus_list.order_by('name')
    elif sort_option == 'name_desc':
        menus_list = menus_list.order_by('-name')

    # Pagination
    paginator = Paginator(menus_list, 9)
    page = request.GET.get('page')
    try:
        menus = paginator.page(page)
    except PageNotAnInteger:
        menus = paginator.page(1)
    except EmptyPage:
        menus = paginator.page(paginator.num_pages)

    # Fetch categories for the filter dropdown
    categories = CuisineType.objects.all()

    context = {
        'menus': menus,
        'search_query': search_query,
        'category_filter': category_filter,
        'sort_option': sort_option,
        'categories': categories,
    }

    return render(request, 'catalog/catalog.html', context)
