from django.db import models

# Create your models here.

class Producto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre", unique=True,primary_key=True)
    cantidad = models.IntegerField()
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
