from django.urls import path
from . import views

urlpatterns = [
    path('', views.carrito, name='carrito'),
    path('add_carrito/<int:producto_id>/', views.add_carrito, name='add_carrito'),
    path('remove_carrito/<int:producto_id>/<int:carrito_item_id>/', views.remove_carrito, name='remove_carrito'),
    path('remove_carrito_item/<int:producto_id>/<int:carrito_item_id>/', views.remove_carrito_item, name='remove_carrito_item'),
    path('checkout/', views.checkout, name='checkout'),
]
