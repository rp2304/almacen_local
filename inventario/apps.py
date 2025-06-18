from django.apps import AppConfig  # Importa la clase base para configurar la aplicación

class InventarioConfig(AppConfig):
    """
    Configuración de la aplicación 'inventario'.
    Define el nombre de la app y el tipo de campo automático para claves primarias.
    """
    name = 'inventario'                          # Nombre de la aplicación en proyecto Django
    default_auto_field = 'django.db.models.BigAutoField'  # Tipo de campo por defecto para PKs
