from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Almacen)
admin.site.register(Producto)
admin.site.register(Existencia)
admin.site.register(Movimiento)
admin.site.register(Ventas)
