from django.shortcuts import render, redirect
from django.http import JsonResponse
from carrito.models import CarritoItem
from .forms import PedidoForm
import datetime
from .models import Pedido, Pagos, PedidoProducto
import json
from store.models import Producto
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# Create your views here.

def pagos(request):
    body = json.loads(request.body)
    order = Pedido.objects.get(user=request.user, is_orderer=False, order_number=body['orderID'])

    payment = Pagos(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_id = order.pedido_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_orderer = True
    order.save()

    # ejecutar la orden del carrito hacia la tabla PedidoProducto
    carrito_items = CarritoItem.objects.filter(user=request.user)

    for item in carrito_items:
        pedidoproducto = PedidoProducto()
        pedidoproducto.pedido_id = order.id
        pedidoproducto.payment = payment
        pedidoproducto.user_id = request.user.id
        pedidoproducto.producto_id = item.producto_id
        pedidoproducto.qty = item.qty
        pedidoproducto.precio_producto = item.producto.precio
        pedidoproducto.orderer = True
        pedidoproducto.save()

        carrito_item = CarritoItem.objects.get(id=item.id)
        producto_variedad = carrito_item.variedades.all()
        pedidoproducto = PedidoProducto.objects.get(id=pedidoproducto.id)
        pedidoproducto.variedad.set(producto_variedad)
        pedidoproducto.save()

        producto = Producto.objects.get(id=item.producto_id)
        producto.stock -= item.qty
        producto.save()

    CarritoItem.objects.filter(user=request.user).delete()

    mail_subject = 'Gracias por su compra'
    body = render_to_string('pedidos/pedido_recieved_email.html', {
        'user': request.user,
        'order': order,
    })

    to_email = request.user.email
    send_email = EmailMessage(mail_subject, body, to=[to_email])
    try:
        send_email.send()
    except Exception as e:
        print(f"Error al enviar correo: {e}")

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }

    return JsonResponse(data)





def ordenar_pedido(request, total=0, quantity=0):
    current_user = request.user
    carrito_items = CarritoItem.objects.filter(user=current_user)
    carrito_count = carrito_items.count()

    if carrito_count <= 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0

    for carrito_item in carrito_items:
        total += (carrito_item.producto.precio * carrito_item.qty)
        quantity += carrito_item.qty

    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = PedidoForm(request.POST)

        if form.is_valid():
            data = Pedido()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.direccion = form.cleaned_data['direccion']
            data.comuna = form.cleaned_data['comuna']
            data.descripcion_pedido = form.cleaned_data['descripcion_pedido']
            data.pedido_total = grand_total
            data.tax = tax 
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            dt = int(datetime.date.today().strftime('%d'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            pedido = Pedido.objects.get(user=current_user, is_orderer=False, order_number=order_number)
            context = {
                'pedido': pedido,
                'carrito_items': carrito_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }

            return render(request, 'pedidos/pagos.html', context)
    else:
        return redirect('checkout')



def pedido_completado(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Pedido.objects.get(order_number=order_number, is_orderer=True)
        orderer_productos = PedidoProducto.objects.filter(pedido_id=order.id)

        subtotal = 0
        for i in orderer_productos:
            subtotal += i.precio_producto*i.qty

        payment = Pagos.objects.get(payment_id=transID)

        context = {
            'order': order,
            'orderer_productos': orderer_productos,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'pedidos/pedido_completado.html', context)
    except(Pagos.DoesNotExist, Pedido.DoesNotExist):
        return redirect('home')
