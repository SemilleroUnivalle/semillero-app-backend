from rest_framework import serializers
from .models import Estudiante
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = [
            '__all__',  # Incluye todos los campos del modelo
        ]
        # No incluir password en los campos editables directamente
        extra_kwargs = {
            'password': {'write_only': True},
            # Si necesitas que algunos campos sean solo lectura
            # 'registration_phase': {'read_only': True},
        }

class EstudianteInicioSesionSerializer(serializers.Serializer):
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

        # Guarda el estudiante para que esté disponible en la vista
        data['student'] = student
        
        return data

