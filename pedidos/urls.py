from django.urls import path
from . import views

urlpatterns = [
    path('ordenar_pedido', views.ordenar_pedido, name="ordenar_pedido"),
    path('pagos', views.pagos, name="pagos"),
    path('pedido_completado/', views.pedido_completado, name="pedido_completado"),
]
