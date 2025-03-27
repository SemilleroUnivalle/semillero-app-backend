from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class StudentManager(BaseUserManager):
    """Manager para manejar la creación de estudiantes"""

    def create_user(self, nombre, apellido, numero_identificacion, email, password=None):
        """Crea y retorna un estudiante con el número de identificación como contraseña"""

        email = self.normalize_email(email)

        student = self.model(
            nombre=nombre,
            apellido=apellido,
            numero_identificacion=numero_identificacion,
            email=email
        )

        # Se usa el número de identificación como contraseña
        student.set_password(numero_identificacion)

        # Imprimir los datos del estudiante antes de guardarlos
        print(f"Datos del estudiante antes de guardar: {student.__dict__}")

        student.save(using=self._db)
        return student

class Student(AbstractBaseUser):
    """Modelo de usuario para estudiantes"""
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    numero_identificacion = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    
    objects = StudentManager()

    # Ahora se inicia sesión con el número de identificación
    USERNAME_FIELD = 'numero_identificacion'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'email']

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.numero_identificacion}"

