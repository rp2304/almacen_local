from django.shortcuts import render, redirect                # Funciones para renderizar plantillas y redirigir
from django.contrib.auth import authenticate, login, logout  # Funciones de autenticación y gestión de sesión
from django.contrib import messages                           # Biblioteca para mensajes flash al usuario
from django.contrib.auth.decorators import login_required     # Decorador para proteger vistas
from django.contrib.admin.views.decorators import staff_member_required  # Decorador para vistas de staff
from django.http import HttpResponse, HttpResponseForbidden   # Respuestas HTTP básicas

from .forms import RegistroUsuarioForm                        # Formulario para registro y edición de usuarios
from .models import Usuario                                   # Modelo de usuario personalizado

def login_view(request):                                      # Vista para el formulario de inicio de sesión
    if request.method == 'POST':                              # Comprueba si el formulario fue enviado
        email = request.POST.get('email')                     # Obtiene el email ingresado
        password = request.POST.get('password')               # Obtiene la contraseña ingresada
        user = authenticate(request, email=email, password=password)  # Valida credenciales
        if user is not None:                                  # Si las credenciales son válidas
            login(request, user)                              # Inicia la sesión del usuario
            if user.is_superuser:                             # Comprueba si es superusuario
                return redirect('/admin/')                    # Redirige al panel de admin de Django
            if user.rol == 'administrador':                   # Si es administrador
                return redirect('panel_administrador')        # Redirige a su panel personalizado
            elif user.rol == 'vendedor':                      # Si es vendedor
                return redirect('/vendedor/')                 # Redirige a la sección de vendedor
            elif user.rol == 'bodega':                        # Si es personal de bodega
                return redirect('/bodega/')                   # Redirige a la sección de bodega
            else:                                             # Cualquier otro rol
                return redirect('/')                          # Redirige a la página principal
        else:                                                 # Credenciales inválidas
            messages.error(request, 'Credenciales inválidas') # Muestra mensaje de error
    return render(request, 'usuarios/login.html')             # Renderiza el formulario de login

def logout_view(request):                                     # Vista para cerrar sesión
    logout(request)                                          # Termina la sesión del usuario
    return redirect('login')                                  # Redirige al formulario de login

@login_required                                              # Solo usuarios autenticados pueden acceder
def vista_vendedor(request):                                  # Vista de bienvenida para vendedores
    return HttpResponse("<h2>Bienvenido, vendedor</h2>")     # Respuesta HTML simple

@staff_member_required                                       # Solo accesible para miembros del staff
def registrar_usuario(request):                               # Vista para registrar nuevos usuarios
    usuarios = Usuario.objects.all().order_by('rol', 'apellido')  # Lista usuarios ordenados

    if request.method == 'POST':                              # Si se envía el formulario
        form = RegistroUsuarioForm(request.POST)              # Crea formulario con datos POST
        if form.is_valid():                                   # Valida el formulario
            usuario = form.save(commit=False)                 # Crea instancia sin guardar
            usuario.set_password(form.cleaned_data['password'])  # Encripta contraseña
            usuario.save()                                    # Guarda el usuario en BD
            messages.success(request, 'Usuario registrado exitosamente.')  # Mensaje de éxito
            return redirect('registrar_usuario')              # Recarga la página
    else:                                                     # Si no es POST
        form = RegistroUsuarioForm()                          # Formulario vacío

    return render(request, 'usuarios/registrar_usuario.html', {  # Renderiza plantilla
        'form': form,                                         # Pasa el formulario
        'usuarios': usuarios                                  # Pasa la lista de usuarios
    })

from django.shortcuts import get_object_or_404                # Función para obtener objetos o 404

@staff_member_required                                       # Solo staff puede editar usuarios
def editar_usuario(request, usuario_id):                      # Vista para editar usuario existente
    usuario = get_object_or_404(Usuario, id=usuario_id)      # Obtiene usuario o error 404
    if request.method == 'POST':                              # Si se envía el formulario
        form = RegistroUsuarioForm(request.POST, instance=usuario)  # Formulario con instancia
        if form.is_valid():                                   # Valida cambios
            usuario = form.save(commit=False)                 # Guarda instancia sin commit
            if form.cleaned_data['password']:                 # Si ingresaron nueva contraseña
                usuario.set_password(form.cleaned_data['password'])  # Encripta nueva contraseña
            usuario.save()                                    # Guarda cambios en BD
            messages.success(request, 'Usuario actualizado exitosamente.')  # Mensaje
            return redirect('registrar_usuario')              # Redirige al listado
    else:                                                     # Si no es POST
        form = RegistroUsuarioForm(instance=usuario)          # Formulario precargado
    usuarios = Usuario.objects.all().order_by('rol', 'apellido')  # Lista actualizada
    return render(request, 'usuarios/registrar_usuario.html', {
        'form': form,                                         # Formulario para editar
        'usuarios': usuarios,                                 # Lista usuarios
        'editando': usuario                                   # Contexto: usuario en edición
    })

@staff_member_required                                       # Solo staff puede eliminar usuarios
def eliminar_usuario(request, usuario_id):                    # Vista para eliminar un usuario
    usuario = get_object_or_404(Usuario, id=usuario_id)      # Obtiene usuario o 404
    if usuario != request.user:                              # Impide auto-eliminación
        usuario.delete()                                     # Elimina el usuario
        messages.success(request, 'Usuario eliminado exitosamente.')  # Mensaje de éxito
    else:
        messages.warning(request, 'No puedes eliminar tu propia cuenta.')  # Alerta
    return redirect('registrar_usuario')                      # Redirige al listado

@login_required                                              # Protege acceso a administrador
def panel_administrador(request):                            # Vista del panel de administrador
    if request.user.rol != 'administrador':                  # Verifica rol
        return HttpResponseForbidden("No tienes permiso para acceder.")  # Deniega
    return render(request, 'usuarios/panel_administrador.html')  # Muestra panel

@login_required                                              # Protege acceso a bodega
def panel_bodega(request):                                    # Vista del panel de bodega
    if request.user.rol != 'bodega':                         # Verifica rol bodega
        return HttpResponseForbidden("Acceso denegado.")     # Deniega acceso
    return render(request, 'usuarios/panel_bodega.html')     # Muestra panel de bodega
