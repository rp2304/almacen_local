# Importaciones de Django para control de acceso y manejo de vistas
from django.contrib.auth.decorators import login_required  # Decorador para requerir usuario autenticado
from django.shortcuts import render, redirect             # Funciones para renderizar plantillas y redirigir
from django.http import HttpResponseForbidden              # Respuesta 403 cuando el usuario no tiene permiso

# Importaciones de los formularios y modelos de la aplicación
from .forms import ProductoForm, MovimientoForm            # Formularios para Producto y Movimiento
from .models import Producto, Movimiento, Categoria        # Modelos de Producto, Movimiento y Categoría

@login_required
def registrar_producto(request):
    # Verifica que el usuario sea administrador; si no, deniega acceso
    if request.user.rol != 'administrador':
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
    # Obtiene todos los productos ordenados por nombre
    productos = Producto.objects.all().order_by('nombre')
    
    if request.method == 'POST':
        # Crea instancia del formulario con los datos enviados y archivos
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            # Guarda el nuevo producto en la base de datos
            form.save()
            # Redirige a la misma vista para limpiar el formulario
            return redirect('registrar_producto')
    else:
        # Si no es POST, instancia un formulario vacío
        form = ProductoForm()
    
    # Renderiza la plantilla con el formulario y la lista de productos
    return render(request, 'inventario/registrar_producto.html', {
        'form': form,
        'productos': productos
    })

@login_required
def ver_stock(request):
    # Solo administradores pueden ver el stock
    if request.user.rol != 'administrador':
        return HttpResponseForbidden("No tienes permiso para ver el stock.")
    
    # Obtiene productos ordenados por nombre
    productos = Producto.objects.all().order_by('nombre')
    # Renderiza la plantilla de stock con los productos
    return render(request, 'inventario/ver_stock.html', {
        'productos': productos
    })

@login_required
def registrar_movimiento(request):
    # Solo administradores y encargados de bodega pueden registrar movimientos
    if request.user.rol not in ['administrador', 'encargado de bodega']:
        return HttpResponseForbidden("No tienes permiso para registrar movimientos.")
    
    # Obtiene movimientos recientes, incluyendo datos del producto relacionado
    movimientos = Movimiento.objects.select_related('producto').order_by('-fecha')
    
    if request.method == 'POST':
        # Crea formulario de movimiento con los datos enviados
        form = MovimientoForm(request.POST)
        if form.is_valid():
            # Crea instancia sin guardar para asignar el usuario que lo realiza
            movimiento = form.save(commit=False)
            movimiento.realizado_por = request.user
            movimiento.save()  # Guarda el movimiento en la base de datos
            return redirect('registrar_movimiento')
    else:
        # Si no es POST, instancia un formulario vacío
        form = MovimientoForm()
    
    # Renderiza la plantilla con el formulario y la lista de movimientos
    return render(request, 'inventario/registrar_movimiento.html', {
        'form': form,
        'movimientos': movimientos
    })

@login_required
def ver_productos_bodega(request):
    # Obtiene el parámetro de categoría enviado por GET
    categoria_id = request.GET.get('categoria')
    # Recupera todas las categorías para el filtro
    categorias = Categoria.objects.all()
    
    if categoria_id:
        # Filtra productos por categoría seleccionada
        productos = Producto.objects.filter(categoria_id=categoria_id)
    else:
        # Si no hay filtro, muestra todos los productos
        productos = Producto.objects.all()
    
    # Renderiza la plantilla con productos, categorías y la categoría seleccionada
    return render(request, 'inventario/ver_productos_bodega.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada': categoria_id
    })

# Método de modelo para comprobar si el stock está por debajo del mínimo
@property
def stock_bajo(self):
    # Retorna True si el stock actual es menor o igual al stock mínimo permitido
    return self.stock <= self.stock_minimo
