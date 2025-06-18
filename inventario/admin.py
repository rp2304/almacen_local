# Importaciones de Django para la interfaz de administración
from django.contrib import admin  # Módulo que permite registrar modelos en el admin

# Importación de los modelos que se desea gestionar desde el admin
from .models import Categoria, Producto  # Modelos de Categoría y Producto

# Registro de Categoria en el sitio de administración
admin.site.register(Categoria)  # Hace que el modelo Categoria sea editable desde el admin

# Registro de Producto en el sitio de administración
admin.site.register(Producto)   # Hace que el modelo Producto sea editable desde el admin
