import datetime
import os
from django.utils.datastructures import MultiValueDictKeyError
from pathlib import Path
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import *
from .forms import *
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import json
from django.contrib import messages

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


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
            almacen = producto_form.cleaned_data['almacen']
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
                if Existencia.objects.all().filter(producto=producto.id,
                                                   almacen=Almacen.objects.get(nombre=almacen).id).count() == 0:
                    e = Existencia(almacen=Almacen.objects.get(nombre=almacen), producto=producto,
                                   cantidad=cantidad)
                    # print("No existe el producto en el almacen")
                    try:
                        e.save()
                    except:
                        # print("Error al guardar existencia")
                        pass
                else:
                    # print("Existe el producto en el almacen")
                    messages.error(request, "Producto ya existente en el almacén " + almacen.nombre)
                    return render(request, 'inventory/producto/create_product.html')
            except:
                # print("Error  guardando producto")
                return render(request, 'inventory/producto/create_product.html', context)
            else:
                # print("Agregado correctmamente")
                return HttpResponseRedirect(reverse('inv:list_product'))
        else:
            if Existencia.objects.all().filter(producto=Producto.objects.get(nombre=producto_form['nombre'].value()).id,
                                               almacen=producto_form['almacen'].value()).count() > 0:
                messages.error(request, "Producto ya existente en el almacén " + Almacen.objects.get(
                    id=producto_form['almacen'].value()).nombre)
                return render(request, 'inventory/producto/create_product.html', context)
    else:
        # print("Es un GET")
        return render(request, 'inventory/producto/create_product.html', context)


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'inventory/producto/delete_product.html'
    success_url = 'inv:list_product'


class ProductoListView(ListView):
    model = Producto
    context_object_name = 'object'
    ordering = ['nombre']
    template_name = 'inventory/producto/list_product.html'


# def update_producto(request, pk):
#     if request.method == 'GET':
#         object = Producto.objects.get(id=int(pk))
#         form = ProductoForm(instance=object)
#         context = {
#             'form': form,
#             'msg': 'update'
#         }
#         return render(request, 'inventory/producto/create_product.html', context)
#     if request.method == 'POST':
#         producto_form = ProductoForm()
#         context = {
#             'form': producto_form,
#         }
#         producto_form = ProductoForm(request.POST)
#         if producto_form.is_valid():
#             pass
#             nombre = producto_form.cleaned_data['nombre']
#             cantidad = producto_form.cleaned_data['cantidad']
#             fecha_entrada = producto_form.cleaned_data['fecha_entrada'].split("-")
#             precio_costo = producto_form.cleaned_data['precio_costo']
#             precio_venta = producto_form.cleaned_data['precio_venta']
#             almacen = producto_form.cleaned_data['almacen']
#             anho = int(fecha_entrada[0])
#             mes = int(fecha_entrada[1])
#             dia = int(fecha_entrada[2])
#             producto = Producto(nombre=nombre,
#                                 cantidad=cantidad,
#                                 fecha_entrada=datetime.datetime(anho, mes, dia),
#                                 precio_costo=precio_costo,
#                                 precio_venta=precio_venta
#                                 )
#
#             try:
#                 producto.save()
#             except:
#                 # print("Error  guardando producto")
#                 return render(request, 'inventory/producto/create_product.html', context)
#         else:
#             if Existencia.objects.all().filter(producto=Producto.objects.get(nombre=producto_form['nombre'].value()).id,
#                                                almacen=producto_form['almacen'].value()).count() > 0:
#                 messages.error(request, "Producto ya existente en el almacén " + Almacen.objects.get(
#                     id=producto_form['almacen'].value()).nombre)
#                 return render(request, 'inventory/producto/create_product.html', context)


def create_almacen(request):
    almacen = AlmacenForm()
    context = {
        'form': almacen,
    }
    if request.method == "POST":
        almacen_form = AlmacenForm(request.POST)
        if almacen_form.is_valid():
            nombre = almacen_form.cleaned_data['nombre']
            es_central = almacen_form.cleaned_data['es_central']
            almacen = Almacen(nombre=nombre, es_central=es_central)
            try:
                almacen.save()
                return HttpResponseRedirect(reverse('inv:list_almacen'))
            except:
                return render(request, 'inventory/almacen/create_almacen.html', context)
        else:
            return render(request, 'inventory/almacen/create_almacen.html', context)
    else:
        return render(request, 'inventory/almacen/create_almacen.html', context)


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
                    if Existencia.objects.filter(almacen=destino.id, producto=producto.id).count() == 0:
                        print("No existe producto en el almacen")
                        e = Existencia(almacen=destino, producto=producto, cantidad=cantidad)
                        e.save()
                    else:
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
                else:
                    context['mess'] = 'err'
                    return render(request, 'inventory/movimiento.html', context)
        else:
            return render(request, 'inventory/almacen/create_almacen.html', context)
    else:
        print("GET")
        return render(request, "inventory/movimiento.html", context)


def import_venta(request):
    if request.method == 'GET':
        return render(request, 'inventory/ventas/ventas.html')
    if request.method == 'POST':
        try:
            myfile = request.FILES['myfile']
            files = os.listdir(MEDIA_ROOT)
            if myfile.name not in files:
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                f = open(os.path.join(MEDIA_ROOT, myfile.name))
                data = json.load(f)
                print(type(data))
                fecha_no_f = myfile.name.split('#')[0].split("-")
                anho = int(fecha_no_f[0])
                mes = int(fecha_no_f[1])
                dia = int(fecha_no_f[2])
                fecha = datetime.datetime(anho, mes, dia),

                almacen = f.name.split('#')[1].split(".")[0]

                for key, value in data.items():
                    almacen = Almacen.objects.get(nombre=almacen)
                    producto = Producto.objects.get(nombre=key)
                    producto.cantidad -= int(value)
                    producto.save()
                    e = Existencia.objects.get(almacen=almacen.id, producto=producto.id)
                    e.cantidad -= int(value)
                    e.save()
                    v = Ventas(existencia=e, fecha=datetime.date(anho, mes, dia), cantidad=int(value))
                    try:
                        v.save()
                        return render(request, 'inventory/ventas/ventas.html', {'msg': 'good'})
                    except:
                        pass
        except MultiValueDictKeyError:
            return render(request, 'inventory/ventas/ventas.html', {'msg': 'empty_upload'})
    else:
        print("Venta existente")
        return render(request, 'inventory/ventas/ventas.html', {'msg': 'error'})


def ventas_periodo(request):
    periodos = VentasPeriodoForm()
    context = {
        'form': periodos,
        'msg': '',
        'data': ''
    }
    if request.method == 'POST':
        form_ventas_periodo = VentasPeriodoForm(request.POST)
        if form_ventas_periodo.is_valid():
            fecha_inicio_raw = form_ventas_periodo.cleaned_data['fecha_inicio']
            fecha_fin_raw = form_ventas_periodo.cleaned_data['fecha_fin']
            ventas = Ventas.objects.filter(fecha__range=[fecha_inicio_raw, fecha_fin_raw])
            data = []
            for i in ventas:
                e = Existencia.objects.get(id=i.existencia.id)
                prod = e.producto
                alm = e.almacen
                data.append([i.fecha, alm, prod, i.cantidad])
            context['data'] = data
            return render(request, 'inventory/ventas/reporte_ventas.html', context)
    else:
        context['msg'] = 'form_request'
        return render(request, 'inventory/ventas/reporte_ventas.html', context)


def stored_products(request):
    if request.method == 'GET':
        p = []
        existencia = Existencia.objects.all()
        for e in existencia:
            if e.almacen.es_central == 'Almacén central':
                p.append(e.producto)
        print("Productos sin exhibir :" + str(p))
        return render(request, 'inventory/productos_sin_exhibir.html', {'productos': p})
