from django.db import models
from django.urls import reverse

# Create your models here.
class Categoria(models.Model):
    categoria_name = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=250, blank=True)
    slug = models.CharField(max_length=100, unique=True)
    cat_image = models.ImageField(upload_to='photos/categorias', blank=True)

    def get_url(self):
        return reverse('productos_por_categoria', args=[self.slug])


    def __str__(self):
        return self.categoria_name
