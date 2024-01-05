from django.db import models
from store.models import Producto, Variedad
from cuentas.models import Cuenta
# Create your models here.

class Carrito(models.Model):
    carrito_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.carrito_id
    

class CarritoItem(models.Model):
    user = models.ForeignKey(Cuenta, on_delete=models.CASCADE, null=True )
    variedades = models.ManyToManyField(Variedad, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, null=True)
    qty = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.producto.precio * self.qty

    def __unicode__(self):
        return self.producto