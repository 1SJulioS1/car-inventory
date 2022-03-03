from django.forms import ModelForm

from .models import Producto

class ProductoForm(ModelForm):
    class Meta:
        model=Producto
        fiels='__all__'
        labels={
            'name':'descripcion'
        }