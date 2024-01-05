from django.shortcuts import render
from store.models import Producto,ReviewRating


def home(request):
    productos = Producto.objects.all().filter(is_available=True).order_by('created_date')

    for producto in productos:
        reviews = ReviewRating.objects.filter(producto_id=producto.id, status=True)

    context = {
        'productos': productos,
        'reviews': reviews,
    }


    return render(request, 'home.html', context)