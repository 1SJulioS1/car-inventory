from django.urls import path, include

from inventory import views

app_name = 'inv'

producto = [
    path('crear-producto/', views.product, name="create_product"),
    path('modificar-producto/<pk>/', views.update_producto, name="update_product"),
    path('eliminar-producto/<pk>/', views.ProductoDeleteView.as_view(), name="delete_product"),
    path('listar-producto/', views.ProductoListView.as_view(), name="list_product"),

]

almacen = [
    path('crear-almacen/', views.create_almacen, name="create_almacen"),
    path('eliminar-almacen/<pk>/', views.AlmacenDeleteView.as_view(), name="delete_almacen"),
    path('listar-almacen/', views.AlmacenListView.as_view(), name="list_almacen"),
]

urlpatterns = [

    path('', views.home, name='Home'),
    path('inst-almacen/<pk>/', views.productos_almacen, name="products_instruments"),
    path('movimiento/', views.movimiento, name='Movimiento'),
    path('producto/', include(producto)),
    path('almacen/', include(almacen))
]
