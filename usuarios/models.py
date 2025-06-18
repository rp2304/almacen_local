from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin  # Clases para personalizar modelo de usuario
from django.db import models                                                             # Clases base para definir campos de modelo

class UsuarioManager(BaseUserManager):                                                   # Administrador personalizado para Usuario
    def create_user(self, email, nombre, apellido, password=None, **extra_fields):        # Método para crear usuarios regulares
        if not email:                                                                    # Verifica que el email sea provisto
            raise ValueError('El usuario debe tener un correo electrónico')              # Lanza error si falta email
        email = self.normalize_email(email)                                              # Normaliza el email (minúsculas, etc.)
        usuario = self.model(email=email, nombre=nombre, apellido=apellido, **extra_fields)  # Crea instancia de Usuario
        usuario.set_password(password)                                                   # Encripta la contraseña
        usuario.save(using=self._db)                                                     # Guarda el usuario en la base de datos
        return usuario                                                                   # Retorna la instancia creada

    def create_superuser(self, email, nombre, apellido, password=None, **extra_fields):   # Método para crear administrador
        extra_fields.setdefault('is_staff', True)                                        # Marca como staff
        extra_fields.setdefault('is_superuser', True)                                    # Marca como superusuario
        return self.create_user(email, nombre, apellido, password, **extra_fields)       # Reusa create_user para creación

class Usuario(AbstractBaseUser, PermissionsMixin):                                       # Modelo personalizado de usuario
    ROLES = (                                                                            # Opciones de rol del usuario
        ('administrador', 'Administrador'),                                             #   Administrador
        ('vendedor', 'Vendedor'),                                                       #   Vendedor
        ('bodega', 'Encargado de Bodega'),                                              #   Encargado de bodega
    )

    email = models.EmailField(unique=True)                                              # Campo de email único
    nombre = models.CharField(max_length=30)                                             # Nombre del usuario
    apellido = models.CharField(max_length=30)                                           # Apellido del usuario
    rol = models.CharField(max_length=20, choices=ROLES, default='vendedor')             # Rol del usuario con valor por defecto

    is_active = models.BooleanField(default=True)                                        # Indica si la cuenta está activa
    is_staff = models.BooleanField(default=False)                                        # Indica si puede acceder al admin

    objects = UsuarioManager()                                                           # Asigna el administrador personalizado

    USERNAME_FIELD = 'email'                                                             # Campo usado como identificador
    REQUIRED_FIELDS = ['nombre', 'apellido']                                             # Campos obligatorios al crear superusuario

    def __str__(self):                                                                   # Representación en texto del usuario
        return f"{self.nombre} {self.apellido} ({self.email})"                           # Muestra nombre completo y email
