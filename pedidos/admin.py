from django.contrib import admin
from .models import Pagos, Pedido, PedidoProducto
# Register your models here.
class PedidoProductoInline(admin.TabularInline):
    model = PedidoProducto
    readonly_fields = ('payment', 'user', 'producto', 'qty', 'precio_producto','orderer')
    extra = 0



class PedidoAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'comuna', 'pedido_total', 'tax', 'status', 'is_orderer', 'created_at']
    list_filter = ['status', 'is_orderer']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [PedidoProductoInline]


admin.site.register(Pagos)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(PedidoProducto)