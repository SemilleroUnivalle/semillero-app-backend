from rest_framework import serializers
from .models import Student
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import AuthenticationFailed

class StudentSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Student"""

    class Meta:
        model = Student
        fields = ['id', 'nombre', 'apellido', 'numero_identificacion', 'email']

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

