from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('categoria/<slug:categoria_slug>/', views.store, name='productos_por_categoria'),
    path('categoria/<slug:categoria_slug>/<slug:producto_slug>/', views.producto_detalle, name='producto_detalle'),
    path('busqueda/', views.busqueda, name='busqueda'),
    path('submit_review/<int:producto_id>/', views.submit_review, name='submit_review'),
] 
