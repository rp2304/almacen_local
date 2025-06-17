from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .forms import ProductoForm
from .models import Producto
from .models import Movimiento
from .forms import MovimientoForm

@login_required
def registrar_producto(request):
    if not request.user.rol == 'administrador':
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

    productos = Producto.objects.all().order_by('nombre')

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('registrar_producto')
    else:
        form = ProductoForm()

    return render(request, 'inventario/registrar_producto.html', {
        'form': form,
        'productos': productos
    })


from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Producto
from django.shortcuts import render

@login_required
def ver_stock(request):
    if request.user.rol != 'administrador':
        return HttpResponseForbidden("No tienes permiso para ver el stock.")

    productos = Producto.objects.all().order_by('nombre')
    return render(request, 'inventario/ver_stock.html', {'productos': productos})


@login_required
def registrar_movimiento(request):
    if request.user.rol not in ['administrador', 'encargado de bodega']:
        return HttpResponseForbidden("No tienes permiso para registrar movimientos.")

    movimientos = Movimiento.objects.select_related('producto').order_by('-fecha')
    
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.realizado_por = request.user
            movimiento.save()
            return redirect('registrar_movimiento')
    else:
        form = MovimientoForm()

    return render(request, 'inventario/registrar_movimiento.html', {
        'form': form,
        'movimientos': movimientos
    })


from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Producto
from django.shortcuts import render

@login_required
def ver_productos_bodega(request):
    if request.user.rol != 'bodega':
        return HttpResponseForbidden("No tienes permiso para ver los productos.")
    
    productos = Producto.objects.all().order_by('nombre')
    return render(request, 'inventario/ver_productos_bodega.html', {'productos': productos})
