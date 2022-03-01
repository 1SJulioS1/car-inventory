from django.core.validators import MinValueValidator
from django.db import models


class Producto(models.Model):
    nombre = models.CharField(
        max_length=100, unique=True, primary_key=True)
    almacen = models.ForeignKey("Almacen", null=True, on_delete=models.SET_NULL)
    cantidad = models.IntegerField(default=0, validators=[
        MinValueValidator(0)
    ])
    fecha_entrada = models.DateTimeField()
    precio_costo = models.DecimalField(decimal_places=2, max_digits=10, default=0, validators=[MinValueValidator(0)])
    precio_venta = models.DecimalField(decimal_places=2, max_digits=10, default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


class Almacen(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Almacenes"
        verbose_name = "Almacén"
