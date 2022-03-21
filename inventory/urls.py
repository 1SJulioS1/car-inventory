from django.urls import path, include

from inventory import views

app_name = 'inv'

producto = [
    path('crear-producto/', views.product, name="create_product"),
    path('listar-producto/', views.ProductoListView.as_view(), name="list_product"),
    path('productos-sin-exhibir/', views.stored_products, name="stored_products"),
    path('actualizar-producto/', views.extract_product, name="update_product_cant"),
    path('actualizar-precio/', views.change_price, name="change_price"),
]

almacen = [
    path('crear-almacen/', views.AlmacenCreateView.as_view(), name="create_almacen"),
    path('update-almacen/<pk>/', views.AlmacenUpdateView.as_view(), name="update_almacen"),
    path('update-almacen-list/', views.AlmacenListUpdate.as_view(), name="update_almacen_list"),
    path('listar-almacen/', views.AlmacenListView.as_view(), name="list_almacen"),
]

venta = [
    path('crear-venta/',views.create_sell,name="crear_venta")

]
urlpatterns = [

    path('', views.home, name='Home'),
    path('inst-almacen/<pk>/', views.productos_almacen, name="products_instruments"),
    path('movimiento/', views.movimiento2, name='Movimiento'),
    path('importar-venta/', views.import_venta, name='import_selling'),
    path('producto/', include(producto)),
    path('almacen/', include(almacen)),
    path('venta/',include(venta)),
    path("ventas_periodo_form/", views.ventas_periodo, name="selling_period_form")
]
