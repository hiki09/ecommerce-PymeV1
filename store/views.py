from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, ReviewRating
from categoria.models import Categoria
from carrito.models import Carrito, CarritoItem
from carrito.views import _carrito_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages
from pedidos.models import PedidoProducto

# Create your views here.
def store(request, categoria_slug=None):
    categorias = None
    productos = None

    if categoria_slug != None:
        categorias = get_object_or_404(Categoria, slug=categoria_slug)
        productos = Producto.objects.filter(categoria=categorias, is_available=True).order_by('id')
        paginator = Paginator(productos, 5)
        pagina = request.GET.get('pagina')
        pagina_productos = paginator.get_page(pagina)
        productos_cant = productos.count()
    else:
        productos = Producto.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(productos, 5)
        pagina = request.GET.get('pagina')
        pagina_productos = paginator.get_page(pagina)
        productos_cant = productos.count()



    context = {
        'productos' : pagina_productos,
        'productos_cant' : productos_cant,

    }


    return render(request, 'store/store.html', context)


def producto_detalle(request, categoria_slug, producto_slug):
    try:
        single_product = Producto.objects.get(categoria__slug=categoria_slug, slug=producto_slug)
        in_carrito = CarritoItem.objects.filter(carrito__carrito_id=_carrito_id(request), producto=single_product).exists()
    except Exception as e:
        raise e
    
    if request.user.is_authenticated:
        try:
            orderproduct = PedidoProducto.objects.filter(user=request.user, producto_id=single_product.id).exists()
        except PedidoProducto.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None
        

    reviews = ReviewRating.objects.filter(producto_id=single_product.id, status=True)


    context = {
        'single_product': single_product,
        'in_carrito' : in_carrito,
        'orderproduct': orderproduct,
        'reviews': reviews,
    }    

    return render(request, 'store/producto_detalle.html', context)


def busqueda(request):
    productos = None
    productos_count = 0

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            productos = Producto.objects.order_by('-created_date').filter(Q(descripcion__icontains=keyword) | Q(nombre_producto__icontains=keyword))
            productos_count = productos.count()
    context = {
        'productos' : productos,
        'productos_count' : productos_count,
    }

    return render(request, 'store/store.html', context)


def submit_review(request, producto_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, producto__id=producto_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Muchas gracias, tu comentario ha sido actualizado')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.producto_id = producto_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Muchas gracias, tu comentario fue enviado con exito!')
                return redirect(url)
