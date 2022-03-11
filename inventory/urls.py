from django.urls import path, include

from inventory import views

app_name = 'inv'

producto = [
    path('crear-producto/', views.product, name="create_product"),
    path('eliminar-producto/<pk>/', views.ProductoDeleteView.as_view(), name="delete_product"),
    path('listar-producto/', views.ProductoListView.as_view(), name="list_product"),
    path('productos-sin-exhibir/',views.stored_products,name="stored_products")
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
    path('importar-venta/', views.import_venta, name='import_selling'),
    path('producto/', include(producto)),
    path('almacen/', include(almacen)),
    path("ventas_periodo_form/", views.ventas_periodo, name="selling_period_form")
]
