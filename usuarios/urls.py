from django.urls import path                   # Importa la función path para definir rutas URL
from . import views                            # Importa el módulo de vistas de la aplicación

urlpatterns = [
    path('login/', views.login_view, name='login'),                        # Ruta para el formulario de inicio de sesión
    path('logout/', views.logout_view, name='logout'),                     # Ruta para cerrar sesión del usuario
    path('vendedor/', views.vista_vendedor, name='vendedor'),              # Ruta de bienvenida para vendedores
    path('registrar/', views.registrar_usuario, name='registrar_usuario'), # Ruta para registrar nuevos usuarios (staff)
    path('editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),   # Ruta para editar usuario existente
    path('eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'), # Ruta para eliminar usuario
    path('panel/', views.panel_administrador, name='panel_administrador'), # Ruta al panel de administrador
    path('bodega/', views.panel_bodega, name='panel_bodega'),              # Ruta al panel de bodega
]
