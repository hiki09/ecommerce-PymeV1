from django.shortcuts import render, get_object_or_404
from .models import Producto
from categoria.models import Categoria

# Create your views here.
def store(request, categoria_slug=None):
    categorias = None
    productos = None

    if categoria_slug != None:
        categorias = get_object_or_404(Categoria, slug=categoria_slug)
        productos = Producto.objects.filter(categoria=categorias, is_available=True)
        productos_cant = productos.count()
    else:
        productos = Producto.objects.all().filter(is_available=True)
        productos_cant = productos.count()



    context = {
        'productos' : productos,
        'productos_cant' : productos_cant,
    }


    return render(request, 'store/store.html', context)


def producto_detalle(request, categoria_slug, producto_slug):
    try:
        single_product = Producto.objects.get(categoria__slug=categoria_slug, slug=producto_slug)
    except Exception as e:
        raise e

    context = {
        'single_product': single_product
    }    

    return render(request, 'store/producto_detalle.html', context)