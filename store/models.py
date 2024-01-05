from django.db import models
from categoria.models import Categoria
from django.urls import reverse
from cuentas.models import Cuenta
from django.db.models import Avg, Count

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
    
    def averageReview(self):
        reviews = ReviewRating.objects.filter(producto=self, status=True).aggregate(average=Avg('rating'))
        avg=0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
    def countReview(self):
        reviews = ReviewRating.objects.filter(producto=self, status=True).aggregate(count=Count('id'))
        count = 0
        if 'count' in reviews and reviews['count'] is not None:  # Verificamos si 'count' está en reviews
            count = int(reviews['count'])

        return count





class VariedadManager(models.Manager):
    def variedad(self):
        return super(VariedadManager, self).filter(variedad_categoria='variedad', is_active=True)




variedad_categorias_choices = (
    ('variedad', 'variedad'),
)



class Variedad(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variedad_categoria = models.CharField(max_length=100, choices=variedad_categorias_choices)
    variedad_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariedadManager()

    def __str__(self):
        return self.variedad_categoria + ':' + self.variedad_value



class ReviewRating(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    user = models.ForeignKey(Cuenta, on_delete=models.CASCADE)  
    subject = models.CharField(max_length=100, blank=True)
    review = models.CharField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject