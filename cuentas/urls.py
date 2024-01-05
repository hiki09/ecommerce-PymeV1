from django.urls import path
from . import views

urlpatterns = [
    path('registrarse/', views.registrarse, name='registrarse'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('perfil/', views.perfil, name='perfil'),
    path('', views.perfil, name='perfil'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('resetpassword_validate/<uidb64>/<token>', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    path('mis_pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('cambiar_contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),
]

