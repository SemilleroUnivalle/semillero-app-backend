from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class StudentManager(BaseUserManager):
    """Manager para manejar la creación de estudiantes"""
    def create_user(self, nombre, apellido, numero_identificacion, email, password=None):
        """Crea y retorna un estudiante con el número de identificación como contraseña"""
        print(f"Datos recibidos: nombre={nombre}, apellido={apellido}, numero_identificacion={numero_identificacion}, email={email}")
        email = self.normalize_email(email)

        student = self.model(
            nombre=nombre,
            apellido=apellido,
            numero_identificacion=numero_identificacion,
            email=email
        )

        # Se usa el número de identificación como contraseña
        student.set_password(numero_identificacion)
        student.save(using=self._db)
        return student

class Student(AbstractBaseUser):
    """Modelo de usuario para estudiantes"""
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    numero_identificacion = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    # Nuevos campos
    registration_phase = models.PositiveSmallIntegerField(default=1)  # 1 = Fase inicial, 2 = Fase completada

    # Campos opcionales para la segunda fase del registro
    genero = models.CharField(max_length=10, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    departamento_residencia = models.CharField(max_length=100, blank=True, null=True)
    comuna = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    estamento = models.CharField(max_length=50, blank=True, null=True)
    discapacidad = models.CharField(max_length=50, blank=True, null=True)
    tipo_discapacidad = models.CharField(max_length=50, blank=True, null=True)
    descripcion_discapacidad = models.TextField(blank=True, null=True)
    
    #Achivos PDF
    Foto = models.FileField(upload_to='fotos/', blank=True, null=True)
    documento_identidad = models.FileField(upload_to='documentos_identidad/', blank=True, null=True)
    constancia_estudios = models.FileField(upload_to='constancias_estudios/', blank=True, null=True)
    comprobante_pago = models.FileField(upload_to='comprobantes_pago/', blank=True, null=True)

    objects = StudentManager()

    # Ahora se inicia sesión con el número de identificación
    USERNAME_FIELD = 'numero_identificacion'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'email']

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.numero_identificacion}"

