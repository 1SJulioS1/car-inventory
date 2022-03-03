import datetime

from django.core.checks import messages
from django.http import HttpResponseRedirect, JsonResponse

from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import *
from django.contrib.messages import *
from .forms import *

def home(request):
    return render(request, "inventory/home.html")

def product(request):
    producto = ProductoForm()
    context = {
        'form': producto,
    }
    if request.method == 'POST':
        producto_form = ProductoForm(request.POST)
        if producto_form.is_valid():
            nombre = producto_form.cleaned_data['nombre']
            cantidad = producto_form.cleaned_data['cantidad']
            fecha_entrada = producto_form.cleaned_data['fecha_entrada'].split("-")
            precio_costo = producto_form.cleaned_data['precio_costo']
            precio_venta = producto_form.cleaned_data['precio_venta']

            anho = int(fecha_entrada[0])
            mes = int(fecha_entrada[1])
            dia = int(fecha_entrada[2])
            producto = Producto(nombre=nombre,
                                cantidad=cantidad,
                                fecha_entrada=datetime.datetime(anho, mes, dia),
                                precio_costo=precio_costo,
                                precio_venta=precio_venta
                                )
            try:
                producto.save()
                return HttpResponseRedirect(reverse('inv:list_product'))
            except:
                return render(request, 'inventory/producto/create_product.html', context)
        else:
            return render(request, 'inventory/producto/create_product.html', context)
    else:
        return render(request, 'inventory/producto/create_product.html', context)



class ProductoUpdateView(UpdateView):
    model = Producto
    fields = ['nombre', 'cantidad', 'fecha_entrada', 'precio_costo', 'precio_venta']
    template_name = 'inventory/producto/update_product.html'
    success_url = 'inv:list_product'


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'inventory/producto/delete_product.html'
    success_url = 'inv:list_product'


class ProductoListView(ListView):
    model = Producto
    context_object_name = 'object'
    ordering = ['nombre']
    template_name = 'inventory/producto/list_product.html'


def create_almacen(request):
    almacen = AlmacenForm()
    context = {
        'form': almacen,
    }
    if request.method == "POST":
        almacen_form = AlmacenForm(request.POST)
        if almacen_form.is_valid():
            nombre = almacen_form.cleaned_data['nombre']
            almacen = Almacen(nombre=nombre)
            try:
                almacen.save()
                return HttpResponseRedirect(reverse('inv:list_almacen'))
            except:
                return render(request, 'inventory/almacen/create_almacen.html', context)
        else:
            return render(request, 'inventory/almacen/create_almacen.html', context)
    else:
        return render(request, 'inventory/almacen/create_almacen.html', context)


class AlmacenUpdateView(UpdateView):
    model = Almacen
    fields = ['nombre']
    template_name = 'inventory/almacen/update_almacen.html'
    success_url = reverse_lazy('inv:list_almacen')


class AlmacenDeleteView(DeleteView):
    model = Almacen
    template_name = 'inventory/almacen/delete_almacen.html'
    success_url = reverse_lazy('inv:list_almacen')


class AlmacenListView(ListView):
    model = Almacen
    context_object_name = 'object'
    ordering = ['nombre']
    template_name = 'inventory/almacen/list_almacen.html'


def productos_almacen(request, pk):
    res = dict()
    existencia = Existencia.objects.all()
    for e in existencia:
        if e.almacen.id == int(pk):
            res[e.producto.nombre] = e.cantidad
    return render(request, 'inventory/productos_almacen.html', {'content': res,
                                                                'almacen': Almacen.objects.get(id=int(pk)).nombre})


def movimiento(request):
    mov = MovimientoForm()
    context = {
        'form': mov,
        'mess': ''
    }
    if request.method == "POST":
        mov_form = MovimientoForm(request.POST)
        if mov_form.is_valid():
            origen = mov_form.cleaned_data['almacen_origen']
            destino = mov_form.cleaned_data['almacen_destino']
            producto = mov_form.cleaned_data['producto']
            cantidad = mov_form.cleaned_data['cantidad']
            if origen == destino:
                context['mess'] = 'doubled'
                return render(request, 'inventory/movimiento.html', context)
            else:
                if Existencia.objects.get(almacen=origen.id, producto=producto.id).cantidad > int(cantidad):
                    mov_instance = Movimiento(almacen_origen=origen, almacen_destino=destino,
                                              producto=producto, cantidad=int(cantidad))
                    e = Existencia.objects.get(almacen=origen.id, producto=producto.id)
                    e.cantidad -= int(cantidad)
                    e.save()
                    e = Existencia.objects.get(almacen=destino.id, producto=producto.id).cantidad
                    e.cantidad += int(cantidad)
                    e.save()
                    try:
                        mov_instance.save()
                        return HttpResponseRedirect(reverse('inv:list_almacen'))
                    except:
                        return render(request, 'inventory/movimiento.html', context)
                elif Existencia.objects.get(almacen=origen.id, producto=producto.id).cantidad == int(cantidad):
                    Existencia.objects.get(almacen=origen.id, producto=producto.id).delete()
                    e = Existencia.objects.get(almacen=destino.id, producto=producto.id).cantidad
                    e.cantidad += int(cantidad)
                    e.save()
                    return render(request, 'inventory/almacen/create_almacen.html', context)
                # elif:
                else:
                    context['mess'] = 'err'
                    return render(request, 'inventory/movimiento.html', context)
        else:
            return render(request, 'inventory/almacen/create_almacen.html', context)
    else:
        print("GET")
        return render(request, "inventory/movimiento.html", context)
