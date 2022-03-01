from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from .models import *


# Create your views here.
def home(request):
    return render(request, "inventory/home.html")


def movimiento(request):
    return render(request, "inventory/movimiento.html")


class ProductoCreateView(CreateView):
    model = Producto
    fields = ['nombre', 'cantidad', 'almacen', 'fecha_entrada', 'precio']
    template_name = 'inventory/producto/create_product.html'
    success_url = 'inv:list_product'


class ProductoUpdateView(UpdateView):
    model = Producto
    fields = ['nombre', 'cantidad', 'almacen', 'fecha_entrada', 'precio']
    template_name = 'inventory/producto/update_product.html'
    success_url = 'inv:list_product'


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'inventory/producto/delete_product.html'
    success_url = reverse_lazy('inv:list_product')


class ProductoListView(ListView):
    model = Producto
    context_object_name = 'object'
    ordering = ['nombre']
    template_name = 'inventory/producto/list_product.html'


class AlmacenCreateView(CreateView):
    model = Almacen
    fields = ['localizacion']
    template_name = 'inventory/almacen/create_almacen.html'
    success_url = 'inv:list_product'


class AlmacenUpdateView(UpdateView):
    model = Almacen
    fields = ['localizacion']
    template_name = 'inventory/almacen/update_almacen.html'
    success_url = 'inv:list_product'


class AlmacenDeleteView(DeleteView):
    model = Almacen
    template_name = 'inventory/almacen/delete_almacen.html'
    success_url = reverse_lazy('inv:list_product')


class AlmacenListView(ListView):
    model = Almacen
    context_object_name = 'object'
    ordering = ['localizacion']
    template_name = 'inventory/almacen/list_almacen.html'
