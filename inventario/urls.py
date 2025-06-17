from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.registrar_producto, name='registrar_producto'),
    path('stock/', views.ver_stock, name='ver_stock'),  # ✅
    path('movimientos/', views.registrar_movimiento, name='registrar_movimiento'),
    path('bodega/productos/', views.ver_productos_bodega, name='ver_productos_bodega'),


]
