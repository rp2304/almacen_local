from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')
            if user.rol == 'administrador':
                return redirect('panel_administrador')
            elif user.rol == 'vendedor':
                return redirect('/vendedor/')
            elif user.rol == 'bodega':
                return redirect('/bodega/')
            else:
                return redirect('/')
        else:
            messages.error(request, 'Credenciales inválidas')
    return render(request, 'usuarios/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def vista_vendedor(request):
    return HttpResponse("<h2>Bienvenido, vendedor</h2>")



from .forms import RegistroUsuarioForm
from django.contrib.admin.views.decorators import staff_member_required
from .models import Usuario

@staff_member_required
def registrar_usuario(request):
    usuarios = Usuario.objects.all().order_by('rol', 'apellido')  # puedes ajustar el orden

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('registrar_usuario')
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'usuarios/registrar_usuario.html', {
        'form': form,
        'usuarios': usuarios
    })


from django.shortcuts import get_object_or_404

@staff_member_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save(commit=False)
            if form.cleaned_data['password']:
                usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('registrar_usuario')
    else:
        form = RegistroUsuarioForm(instance=usuario)
    usuarios = Usuario.objects.all().order_by('rol', 'apellido')
    return render(request, 'usuarios/registrar_usuario.html', {
        'form': form,
        'usuarios': usuarios,
        'editando': usuario
    })

@staff_member_required
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if usuario != request.user:  # Evita que el jefe se elimine a sí mismo
        usuario.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
    else:
        messages.warning(request, 'No puedes eliminar tu propia cuenta.')
    return redirect('registrar_usuario')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseForbidden

@login_required
def panel_administrador(request):
    if request.user.rol != 'administrador':
        return HttpResponseForbidden("No tienes permiso para acceder.")
    return render(request, 'usuarios/panel_administrador.html')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def panel_bodega(request):
    if request.user.rol != 'bodega':
        return HttpResponseForbidden("Acceso denegado.")
    return render(request, 'usuarios/panel_bodega.html')
