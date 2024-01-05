from django.db import models
from cuentas.models import Cuenta
from store.models import Producto, Variedad

# Create your models here.
class Pagos(models.Model):
    user = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id
    

class Pedido(models.Model):
    STATUS = (
        ('New', 'Nuevo'),
        ('Accepted', 'Aceptado'),
        ('Completed', 'Completado'),
        ('Cancelled', 'Cancelado'),
    )

    user = models.ForeignKey(Cuenta, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Pagos, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    comuna = models.CharField(max_length=50)
    descripcion_pedido = models.CharField(max_length=200, blank=True)
    pedido_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=50, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_orderer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def direccion_envio(self):
        return f'{self.direccion} {self.comuna}'

    def __str__(self):
        return self.first_name
    

class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    payment = models.ForeignKey(Pagos, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variedad = models.ManyToManyField(Variedad, blank=True)
    qty = models.IntegerField()
    precio_producto = models.FloatField()
    orderer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.producto.nombre_producto