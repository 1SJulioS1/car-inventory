from django.urls import path

from inventory import views

urlpatterns = [
    path('',views.home, name='Home'),
    path('productos',views.productos, name='Productos'),
    path('almacen',views.almacen, name='Almacen'),
    path('movimiento',views.movimiento, name='Movimiento'),
]