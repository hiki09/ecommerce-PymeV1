from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['first_name', 'last_name', 'phone', 'email', 'direccion', 'comuna', 'descripcion_pedido']