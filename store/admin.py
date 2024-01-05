from django.contrib import admin
from .models import Producto, Variedad, ReviewRating
# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre_producto', 'precio', 'stock', 'categoria', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('nombre_producto',)}


class VariedadAdmin(admin.ModelAdmin):
    list_display = ('producto', 'variedad_categoria', 'variedad_value', 'is_active' )
    list_editable = ('is_active',)
    list_filter = ('producto', 'variedad_categoria', 'variedad_value', 'is_active' )


admin.site.register(Producto, ProductoAdmin)
admin.site.register(Variedad, VariedadAdmin)
admin.site.register(ReviewRating)