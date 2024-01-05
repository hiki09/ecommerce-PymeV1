from django.contrib import admin
from . models import Carrito, CarritoItem
# Register your models here.
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('carrito_id', 'date_added')

class CarritoItemAdmin(admin.ModelAdmin):   
    list_display = ('producto', 'carrito', 'qty', 'is_active') 



admin.site.register(Carrito, CarritoAdmin)
admin.site.register(CarritoItem, CarritoItemAdmin)