from django.apps import AppConfig                     # Importa la clase base para la configuración de la app

class UsuariosConfig(AppConfig):                       # Define la configuración de la aplicación 'usuarios'
    name = 'usuarios'                                  # Nombre de la aplicación en el proyecto Django
    default_auto_field = 'django.db.models.BigAutoField'  # Tipo de campo por defecto para claves primarias
