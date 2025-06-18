from django import forms # Importa el módulo de formularios de Django
from .models import Usuario # Importa el modelo de usuario personalizado

class RegistroUsuarioForm(forms.ModelForm):
     #Campo adicional para contraseña
    password = forms.CharField(widget=forms.PasswordInput)# Usa widget para ocultar la entrada

    class Meta:
        model = Usuario  # Modelo asociado al formulario
        """Campos a incluir en el formulario de registro"""
        fields = ['nombre', 'apellido', 'email', 'password', 'rol']
