from rest_framework import serializers
from .models import Student
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator

class StudentSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Student"""
    numero_identificacion = serializers.CharField(
        validators=[UniqueValidator(queryset=Student.objects.all())]
    )
    
    class Meta:
        model = Student
        fields = ['id', 'nombre', 'apellido', 'numero_identificacion', 'email']

class StudentRegistrationPhase2Serializer(serializers.ModelSerializer):
    """Serializer para la segunda fase de registro (información complementaria)"""
    class Meta:
        model = Student
        fields = [
            'genero', 'fecha_nacimiento', 'telefono', 'celular',
            'departamento_residencia', 'comuna', 'direccion',
            'estamento', 'discapacidad', 'tipo_discapacidad',
            'descripcion_discapacidad'
        ]
        
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.registration_phase = 2  # Actualizar a fase completa
        instance.save()
        return instance

class StudentPhase2FilesSerializer(serializers.ModelSerializer):
    """Serializer para la carga de archivos en la fase 2"""
    class Meta:
        model = Student
        fields = ['Foto', 'documento_identidad', 'constancia_estudios', 'comprobante_pago']
        
class StudentLoginSerializer(serializers.Serializer):
    numero_identificacion = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        from .models import Student
        numero_identificacion = data.get('numero_identificacion')
        password = data.get('password')

        # Agregar un print para ver los datos recibidos
        print(f"Datos recibidos: numero_identificacion={numero_identificacion}, password={password}")

        try:
            student = Student.objects.get(numero_identificacion=numero_identificacion)
        except Student.DoesNotExist:
            raise AuthenticationFailed('Número de identificación o contraseña incorrectos.')

        if not check_password(password, student.password):
            print(f"Contraseña ingresada: {password}, Contraseña almacenada: {student.password}")
            raise AuthenticationFailed('Número de identificación o contraseña incorrectos.')

        return {
            'id': student.id,
            'nombre': student.nombre,
            'apellido': student.apellido,
            'numero_identificacion': student.numero_identificacion,
            'email': student.email,
        }

