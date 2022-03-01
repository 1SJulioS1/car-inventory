from django.urls import path, include

from inventory import views

app_name = 'inv'

producto = [
    path('crear-producto/', views.ProductoCreateView.as_view(), name="create_product"),
    path('modificar-producto/', views.ProductoUpdateView.as_view(), name="update_product"),
    path('eliminar-producto/', views.ProductoDeleteView.as_view(), name="delete_product"),
    path('listar-producto/', views.ProductoListView.as_view(), name="list_product"),

]

almacen = [
    path('crear-almacen/', views.AlmacenCreateView.as_view(), name="create_almacen"),
    path('modificar-almacen/', views.AlmacenUpdateView.as_view(), name="update_almacen"),
    path('eliminar-almacen/', views.AlmacenDeleteView.as_view(), name="delete_almacen"),
    path('listar-almacen/', views.AlmacenListView.as_view(), name="list_almacen"),

]

urlpatterns = [
    path('', views.home, name='Home'),
    path('movimiento/', views.movimiento, name='Movimiento'),
    path('producto/', include(producto)),
    path('almacen/', include(almacen))
]
