# Importaciones de Django para definir formularios basados en modelos
from django import forms
from .models import Producto
from .models import Movimiento # Importación de los modelos utilizados en los formularios

class ProductoForm(forms.ModelForm):
    """Formulario para crear o editar instancias de Producto."""
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'categoria', 'precio_unitario', 'stock', 'imagen']
        # Área de texto con 3 filas para descripción
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            # Permite seleccionar un solo archivo
            'imagen': forms.ClearableFileInput(attrs={'multiple': False}),
        }
        labels = {
            'nombre': 'Nombre del Producto',
            'descripcion': 'Descripción',
            'categoria': 'Categoría',
            'precio_unitario': 'Precio Unitario',
            'stock': 'Stock Disponible',
            'imagen': 'Imagen del Producto',
        }

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['producto', # Producto al que afecta el movimiento
                'tipo',       # Tipo de movimiento: entrada o salida
                'cantidad']   # Cantidad de unidades a mover