from django import template
from store.models import *

register = template.Library()


# Otasi bor kategoriyalarni chiqarib beradi !
@register.simple_tag()
def get_categories():
    return Category.objects.filter(parent=True)


# Otasi yogini olib chiqadi !
@register.simple_tag()
def get_categories_gl():
    return Category.objects.filter(parent=None)


# Glavniy kategoriyaga tegishli kategoriyani olib beradi (subcategories)
@register.simple_tag()
def get_subcategories(category):
    return Category.objects.filter(parent=category)


@register.simple_tag()
def get_sorted():
    sorters = [
        {
            'title': 'Price',
            'sorters': [
                ('price', 'Cheap'),
                ('-price', 'Expensive'),
            ]
        },
        {
            'title': 'Color',
            'sorters': [
                ('color', 'A - Z'),
                ('-color', 'Z - A'),
            ]
        },
        {
            'title': 'Size',
            'sorters': [
                ('size', 'Small'),
                ('-size', 'Large'),
            ]
        }
    ]
    return sorters


# like bosilgan produktlani ajratish
@register.simple_tag()
def get_favourite_products(user):
    fav = FavouriteProducts.objects.filter(user=user)
    products = [i.product for i in fav]
    return products
