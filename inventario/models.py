# impoetaciones de django para definir modelos y ajustar el usuario de la configuración
from django.db import models            #clases base para definir modelos
from django.conf import settings        # para  obtener el modelo de usuario activo

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)  # campo de texto corto para el nombre de la categoria

    def _str_(self):   # Devuelve el nombre de la categoría al mostrarla en admin o en consola
        return self.nombre    
    
    
class Producto(models.Model):
    nombre = models.CharField(max_length=150)  # Nombre del producto, hasta 150 caracteres
    descripcion = models.TextField(blank=True)  # Texto libre para descripción; puede quedar vacío
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE) # Relación muchos-a-uno con Categoria
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2) # Hasta 10 dígitos en total  Con 2 decimales (por ejemplo, 99999999.99)
    stock = models.PositiveIntegerField(default=0) # Cantidad en inventario; no puede ser negativa
    stock_minimo = models.PositiveIntegerField(default=5) # Cantidad mínima para alertar de bajo stock; no puede ser negativa
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True) # Carpeta dentro de MEDIA_ROOT donde se guardan las imágenes, Permite valor nulo en la base, Permite omitirlo en formularios

    def __str__(self):
        return self.nombre # Muestra el nombre del producto en interfaces y consola
    


class Movimiento(models.Model):
    # Opciones posibles para tipo de movimiento
    TIPO_CHOICES = [ 
        ('entrada', 'Entrada'),# Suma stock
        ('salida', 'Salida'), # Resta stock
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE) # Relación con el producto afectado, Si se borra el producto, también el movimiento
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES) # Texto corto para 'entrada' o 'salida', Restringe a los valores definidos arriba 
    cantidad = models.PositiveIntegerField() # Cantidad de unidades a entrar o salir
    fecha = models.DateTimeField(auto_now_add=True) # Fecha y hora en que se crea el registro
    realizado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True) # Usuario que ejecuta el movimiento, Si se borra el usuario, deja campo en NULL, Si se borra el usuario, deja campo en NULL

    def save(self, *args, **kwargs):
        # Ajusta el stock del producto según el tipo de movimiento antes de guardar
        if self.tipo == 'entrada':
            self.producto.stock += self.cantidad
        elif self.tipo == 'salida':
            self.producto.stock -= self.cantidad
        self.producto.save() # Guarda el nuevo stock en la base
        super().save(*args, **kwargs) # Finalmente guarda el movimiento

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"
