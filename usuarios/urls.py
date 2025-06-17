from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('vendedor/', views.vista_vendedor, name='vendedor'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('panel/', views.panel_administrador, name='panel_administrador'),
    path('bodega/', views.panel_bodega, name='panel_bodega'),



]
