from django.shortcuts import render, redirect, get_object_or_404
from store.models import Producto, Variedad
from .models import Carrito, CarritoItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.

def _carrito_id(request):
    carrito = request.session.session_key
    if not carrito:
        carrito = request.session.create()
    return carrito



def add_carrito(request, producto_id):
    producto = Producto.objects.get(id=producto_id)

    current_user = request.user

    if current_user.is_authenticated:
        #Bloque para logica de carrito de compras cuando el usuario inicio sesion
        producto_variedad = []

        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variedad = Variedad.objects.get(producto=producto, variedad_categoria__iexact=key, variedad_value__iexact=value)
                    producto_variedad.append(variedad)
                except:
                    pass


        is_carrito_item_exists = CarritoItem.objects.filter(producto=producto, user=current_user).exists()

        if is_carrito_item_exists:
            carrito_item = CarritoItem.objects.filter(producto=producto, user=current_user)

            ex_var_list = []
            id = []
            for item in carrito_item:
                existing_variedad = item.variedades.all()
                ex_var_list.append(list(existing_variedad))
                id.append(item.id)

            if producto_variedad in ex_var_list:
                index = ex_var_list.index(producto_variedad)
                item_id = id[index]
                item = CarritoItem.objects.get(producto=producto, id=item_id)
                item.qty += 1
                item.save()
            else:
                item = CarritoItem.objects.create(producto=producto, qty=1, user=current_user)
                if len(producto_variedad) > 0 :
                    item.variedades.clear()
                    item.variedades.add(*producto_variedad)
                item.save()
                
        else:
            carrito_item = CarritoItem.objects.create(
                producto = producto,
                qty = 1,
                user = current_user,
            )
            if len(producto_variedad) > 0 :
                carrito_item.variedades.clear()
                carrito_item.variedades.add(*producto_variedad)
            carrito_item.save()

        return redirect('carrito') 
    

    else:

        producto_variedad = []

        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variedad = Variedad.objects.get(producto=producto, variedad_categoria__iexact=key, variedad_value__iexact=value)
                    producto_variedad.append(variedad)
                except:
                    pass



        try:
            carrito = Carrito.objects.get(carrito_id=_carrito_id(request))
        except Carrito.DoesNotExist:
            carrito = Carrito.objects.create(
                carrito_id = _carrito_id(request)
            )
        carrito.save()

        is_carrito_item_exists = CarritoItem.objects.filter(producto=producto, carrito=carrito).exists()
        if is_carrito_item_exists:
            carrito_item = CarritoItem.objects.filter(producto=producto,carrito=carrito)

            ex_var_list = []
            id = []
            for item in carrito_item:
                existing_variedad = item.variedades.all()
                ex_var_list.append(list(existing_variedad))
                id.append(item.id)

            if producto_variedad in ex_var_list:
                index = ex_var_list.index(producto_variedad)
                item_id = id[index]
                item = CarritoItem.objects.get(producto=producto, id=item_id)
                item.qty += 1
                item.save()
            else:
                item = CarritoItem.objects.create(producto=producto, qty=1, carrito=carrito)
                if len(producto_variedad) > 0 :
                    item.variedades.clear()
                    item.variedades.add(*producto_variedad)
                item.save()
                
        else:
            carrito_item = CarritoItem.objects.create(
                producto = producto,
                qty = 1,
                carrito = carrito
            )
            if len(producto_variedad) > 0 :
                carrito_item.variedades.clear()
                carrito_item.variedades.add(*producto_variedad)
            carrito_item.save()

        return redirect('carrito') 


def remove_carrito(request, producto_id, carrito_item_id):
    producto = get_object_or_404(Producto, id=producto_id)

    try:
        if request.user.is_authenticated:
            carrito_item = CarritoItem.objects.get(producto=producto, user=request.user, id=carrito_item_id)
        else:
            carrito = Carrito.objects.get(carrito_id=_carrito_id(request))
            carrito_item = CarritoItem.objects.get(producto=producto, carrito=carrito, id=carrito_item_id)
        if carrito_item.qty > 1:
            carrito_item.qty -= 1
            carrito_item.save()
        else:
            carrito_item.delete()
    except:
        pass
    
    return redirect('carrito')


def remove_carrito_item(request, producto_id, carrito_item_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.user.is_authenticated:
        carrito_item = CarritoItem.objects.get(producto=producto, user=request.user, id=carrito_item_id)
    else:
        carrito = Carrito.objects.get(carrito_id=_carrito_id(request))
        carrito_item = CarritoItem.objects.get(producto=producto, carrito=carrito, id=carrito_item_id)
        
    carrito_item.delete()
    return redirect('carrito')


def carrito(request, total=0, quantity=0, carrito_items=None):
    tax = 0  # Inicializa tax fuera del bloque try para evitar errores con las sesiones
    gran_total = 0  # lo mismo para gran_total
    

    try:
        if request.user.is_authenticated:
            carrito_items = CarritoItem.objects.filter(user=request.user, is_active=True)
        else:
            carrito = Carrito.objects.get(carrito_id=_carrito_id(request))
            carrito_items = CarritoItem.objects.filter(carrito=carrito, is_active=True)

        for carrito_item in carrito_items:
            total += (carrito_item.producto.precio * carrito_item.qty)
            quantity += carrito_item.qty
        tax = (2*total)/100
        gran_total = total + tax

    except ObjectDoesNotExist:
        pass #ignorara la excepcion

    context = {
        'total': total,
        'quantity': quantity,
        'carrito_items': carrito_items,
        'tax' : tax,
        'gran_total' : gran_total,
    }

    return render(request, 'store/carrito.html', context)



@login_required(login_url='login')
def checkout(request, total=0, quantity=0, carrito_items=None):
    tax = 0  # Inicializa tax fuera del bloque try para evitar errores con las sesiones
    gran_total = 0  # lo mismo para gran_total
    

    try:
        
        if request.user.is_authenticated:
            carrito_items = CarritoItem.objects.filter(user=request.user, is_active=True)
        else:
            carrito = Carrito.objects.get(carrito_id=_carrito_id(request))
            carrito_items = CarritoItem.objects.filter(carrito=carrito, is_active=True)

        for carrito_item in carrito_items:
            total += (carrito_item.producto.precio * carrito_item.qty)
            quantity += carrito_item.qty
        tax = (2*total)/100
        gran_total = total + tax

    except ObjectDoesNotExist:
        pass #ignorara la excepcion

    context = {
        'total': total,
        'quantity': quantity,
        'carrito_items': carrito_items,
        'tax' : tax,
        'gran_total' : gran_total,
    }

    return render(request, 'store/checkout.html', context)


    