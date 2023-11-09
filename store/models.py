from django.db import models
from categoria.models import Categoria
from django.urls import reverse

# Create your models here.
class Producto(models.Model):
    nombre_producto = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(max_length=200, blank=True)
    precio = models.IntegerField()
    imagenes = models.ImageField(upload_to='photos/productos')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    def get_url(self):
        return reverse('producto_detalle', args=[self.categoria.slug, self.slug])


    def __str__(self):
        return self.nombre_producto

