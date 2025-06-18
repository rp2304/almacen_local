from django.urls import path  # Importa la función path para definir rutas URL
from . import views           # Importa el módulo de vistas de la aplicación

urlpatterns = [
    path('productos/', views.registrar_producto, name='registrar_producto'),           # Ruta para registrar y listar productos
    path('stock/', views.ver_stock, name='ver_stock'),                                 # Ruta para ver el stock de productos
    path('movimientos/', views.registrar_movimiento, name='registrar_movimiento'),     # Ruta para registrar movimientos de inventario
    path('bodega/productos/', views.ver_productos_bodega, name='ver_productos_bodega'),# Ruta para filtrar y ver productos en bodega
]
