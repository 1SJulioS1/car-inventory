from django.core.validators import MinValueValidator
from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=20, unique=True)
    cantidad = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    fecha_entrada = models.DateField()
    precio_costo = models.DecimalField(decimal_places=2, max_digits=10, default=0, validators=[MinValueValidator(0)])
    precio_venta = models.DecimalField(decimal_places=2, max_digits=10, default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


class Almacen(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    es_central = models.TextField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Almacenes"
        verbose_name = "Almacén"


class Existencia(models.Model):
    almacen = models.ForeignKey("Almacen", on_delete=models.CASCADE)
    producto = models.ForeignKey("Producto", on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name_plural = "Existencia"
        verbose_name = "Existencias"
        unique_together = ['almacen', 'producto']


class Movimiento(models.Model):
    almacen_origen = models.ForeignKey("Almacen", on_delete=models.CASCADE, related_name="almacen_origen")
    almacen_destino = models.ForeignKey("Almacen", on_delete=models.CASCADE, related_name="almacen_destino")
    producto = models.ForeignKey("Producto", on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name_plural = "Movimientos"
        verbose_name = "Movimiento"


class Ventas(models.Model):
    cantidad = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    fecha = models.DateField()
    existencia = models.ForeignKey("Existencia", on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "Existencia"
        verbose_name = "Existencias"
