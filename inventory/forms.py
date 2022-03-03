from django import forms
from .models import *


class ProductoForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'nombre_producto',
                'id': 'nombre'
            }
        )
    )
    cantidad = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'cantidad',
                'pattern': '[0-9]+'
            }
        )
    )
    fecha_entrada = forms.CharField(
        widget=forms.TextInput(
            attrs={'type': 'date',
                   'class': 'form-control',
                   'id': 'fecha',
                   'placeholder': 'Fecha de aquisición'
                   }
        )
    )

    precio_costo = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'precio_costo',
                'placeholder': 'Precio de Compra',
                'pattern': '[0-9]*(.[0-9]+)?'
            }
        )
    )
    precio_venta = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'precio_costo',
                'placeholder': 'Precio de Venta',
                'pattern': '[0-9]*(.[0-9]+)?'
            }
        )
    )

    class Meta:
        model = Producto
        fields = '__all__'


class AlmacenForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'nombre_producto',
                'id': 'nombre'
            }
        )
    )

    class Meta:
        model = Almacen
        fields = '__all__'


class MovimientoForm(forms.ModelForm):
    almacen_origen = forms.ModelChoiceField(
        queryset=Almacen.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    almacen_destino = forms.ModelChoiceField(
        queryset=Almacen.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    cantidad = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'pattern': '[0-9]+'
        }
    )
    )

    class Meta:
        model = Movimiento
        fields = '__all__'
