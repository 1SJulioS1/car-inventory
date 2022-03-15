import datetime
import os

from django.core import serializers
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
                    try:
                        e.save()
                    except:
                        # print("Error al guardar existencia")
                        pass
                else:
                    messages.error(request, "Producto ya existente en el almacén " + almacen.nombre)
                    return render(request, 'inventory/producto/create_product.html')
            except:
                return render(request, 'inventory/producto/create_product.html', context)
            else:

                return HttpResponseRedirect(reverse('inv:list_product'))
        else:

            if Existencia.objects.filter(producto=Producto.objects.get(nombre=request.POST['nombre']),
                                         almacen=Almacen.objects.get(id=request.POST['almacen'])).count() > 0:
                messages.error(request, "Producto ya existente en el almacén " + Almacen.objects.get(
                    id=producto_form['almacen'].value()).nombre)
                return render(request, 'inventory/producto/create_product.html', {'form': producto_form})
            else:
                e = Existencia(producto=Producto.objects.get(nombre=producto_form['nombre'].value()),
                               almacen=Almacen.objects.get(id=producto_form['almacen'].value()),
                               cantidad=request.POST['cantidad'])
                e.save()
                return HttpResponseRedirect(reverse('inv:list_product'))

    else:
        return render(request, 'inventory/producto/create_product.html', context)


class ProductoListView(ListView):
    model = Producto
    context_object_name = 'object'
    ordering = ['nombre']
    template_name = 'inventory/producto/list_product.html'


class AlmacenCreateView(CreateView):
    model = Almacen
    form_class = AlmacenForm
    success_url = reverse_lazy('inv:list_almacen')
    template_name = 'inventory/almacen/create_almacen.html'

    def form_invalid(self, form):
        messages.error(self.request, "Almacén ya existente, introduzca otro nombre")
        return self.render_to_response(self.get_context_data(form=form))


class AlmacenListView(ListView):
    model = Almacen
    context_object_name = 'object'
    ordering = ['nombre']
    template_name = 'inventory/almacen/list_almacen.html'
    success_url = reverse_lazy('metr:update_almacen_list')


class AlmacenListUpdate(ListView):
    model = Almacen
    context_object_name = 'object'
    ordering = ['nombre']
    template_name = 'inventory/almacen/list_almacen_upd.html'


class AlmacenUpdateView(UpdateView):
    model = Almacen
    form_class = AlmacenForm
    success_url = reverse_lazy('inv:update_almacen_list')
    pk_url_kwarg = 'pk'
    template_name = 'inventory/almacen/update_almacen.html'

    def form_invalid(self, form):
        messages.error(self.request, "Almacén ya existente, introduzca otro nombre")
        return self.render_to_response(self.get_context_data(form=form))


def productos_almacen(request, pk):
    res = dict()
    existencia = Existencia.objects.all()
    for e in existencia:
        if e.almacen.id == int(pk):
            res[e.producto.nombre] = e.cantidad
    return render(request, 'inventory/productos_almacen.html', {'content': res,
                                                                'almacen': Almacen.objects.get(id=int(pk)).nombre})


def movimiento2(request):
    js = serializers.get_serializer('json')()
    prod = js.serialize(Producto.objects.all(), ensure_ascii=False)
    almacen = js.serialize(Almacen.objects.all(), ensure_ascii=False)
    existencia = js.serialize(Existencia.objects.all(), ensure_ascii=False)
    if (request.method == "GET"):
        return render(request, 'inventory/movimiento2.html',
                      {'prod': prod, 'almacen': almacen, 'existencia': existencia})
    else:
        alm_origen_post = request.POST['almacen-origen']
        alm_origen = Almacen.objects.get(nombre=alm_origen_post)
        alm_destino_post = request.POST['almacen-destino']
        alm_destino = Almacen.objects.get(nombre=alm_destino_post)
        prod_post = request.POST['producto']
        producto = Producto.objects.get(nombre=prod_post)
        cant_new_post = int(request.POST['cant-mov'])
        cant_old_post = int(request.POST['cantidad-disp'])
        if (cant_old_post < cant_new_post):
            messages.error(request,
                           "Cantidad disponible menor que la que se quiere mover. Inserte otra")
            return render(request, 'inventory/movimiento2.html',
                          {'prod': prod, 'almacen': almacen, 'existencia': existencia})
        else:
            mov_instance = Movimiento(almacen_origen=alm_origen, almacen_destino=alm_destino,
                                      producto=producto, cantidad=cant_new_post)
            e = Existencia.objects.get(almacen=alm_origen, producto=producto)
            e.cantidad -= cant_new_post
            e.save()
            mov_instance.save()
            try:
                e1 = Existencia.objects.get(almacen=alm_destino.id, producto=producto.id)
            except:
                e1 = Existencia(almacen=alm_destino, producto=producto, cantidad=cant_new_post)
                e1.save()
                return HttpResponseRedirect(reverse('inv:list_almacen'))
            else:
                e1.cantidad += cant_new_post
                e1.save()
                return HttpResponseRedirect(reverse('inv:list_almacen'))


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
            # Agregar control de excepcion
            # 1- Cuando ya existe una venta en ese dia(ValueError)           
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


def extract_product(request):
    js = serializers.get_serializer('json')()
    producto = js.serialize(Producto.objects.all(), ensure_ascii=False)
    almacen = js.serialize(Almacen.objects.all(), ensure_ascii=False)
    existencia = js.serialize(Existencia.objects.all(), ensure_ascii=False)
    if request.method == 'GET':
        print('get')
        return render(request, 'inventory/producto/extract_product.html',
                      {'producto': producto, 'almacen': almacen, 'existencia': existencia})
    else:
        prod = request.POST['producto']
        alm = request.POST['almacen']
        cant = int(request.POST['cantidad-new'])
        p = Producto.objects.get(nombre=prod)
        a_id = Almacen.objects.get(nombre=alm).id
        e = Existencia.objects.get(producto=p.id, almacen=a_id)
        e.cantidad = e.cantidad - cant
        p.cantidad = p.cantidad - cant
        e.save()
        p.save()
        return HttpResponseRedirect(reverse('inv:list_product'))


def change_price(request):
    js = serializers.get_serializer('json')()
    producto = js.serialize(Producto.objects.all(), ensure_ascii=False)
    if request.method == 'GET':
        return render(request, 'inventory/producto/change_price.html', {'producto': producto})
    else:
        prod = request.POST['producto']
        old_price = request.POST['old-price']
        new_price = request.POST['new-price']
        p = Producto.objects.get(nombre=prod)
        p.precio_venta = int(new_price)
        p.save()
        return HttpResponseRedirect(reverse('inv:list_product'))
