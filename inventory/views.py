from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return render(request, "inventory/home.html")

def productos(request):
    return render(request, "inventory/productos.html")

def almacen(request):
    return render(request, "inventory/almacen.html")

def movimiento(request):
    return render(request, "inventory/movimiento.html")