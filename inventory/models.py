from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Producto(models.Model):
    nombre = models.CharField(
        max_length=100, unique=True, primary_key=True)
    cantidad = models.IntegerField(default=0, validators=[
        MinValueValidator(0)
    ]
    )
    almacen = models.ForeignKey("Almacen", null=True, on_delete=models.SET_NULL)
    fechar_entrada = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


class Almacen(models.Model):
    localizacion = models.TextField(
        max_length=100, 
        unique=True,
    )

    def __str__(self):
        return self.localizacion
    
    class Meta:
        verbose_name_plural = "Almacenes"
        verbose_name = "Almacén"