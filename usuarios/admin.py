from django.contrib import admin                                        # Importa módulo de administración de Django
from django.contrib.auth.admin import UserAdmin                         # Importa clase base para administración de usuarios
from .models import Usuario                                              # Importa el modelo de usuario personalizado

class UsuarioAdmin(UserAdmin):                                           # Define configuración de admin para Usuario
    model = Usuario                                                      # Asocia el modelo Usuario
    list_display = ('email', 'nombre', 'apellido', 'rol', 'is_staff')    # Columnas que se muestran en la lista
    list_filter = ('rol', 'is_staff')                                    # Filtros laterales por rol y staff

    fieldsets = (                                                        # Agrupaciones de campos para edición
        (None, {'fields': ('email', 'password')}),                       # Sección principal: email y contraseña
        ('Información personal', {'fields': ('nombre', 'apellido', 'rol')}),  # Datos personales
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),  # Permisos y grupos
    )

    add_fieldsets = (                                                     # Campos al crear un nuevo usuario
        (None, {
            'classes': ('wide',),                                        # Clase CSS para dar más espacio
            'fields': ('email', 'nombre', 'apellido', 'rol', 'password1', 'password2'),  # Campos obligatorios al crear
        }),
    )

    search_fields = ('email',)                                           # Campo(s) para búsqueda rápida
    ordering = ('email',)                                                # Orden por defecto en la lista

# Registra Usuario con la configuración personalizada en el sitio de admin
admin.site.register(Usuario, UsuarioAdmin)                              # Hace el modelo visible en el admin  
