from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

User = get_user_model()
from .models import Estudiante
from curse.models import Modulo

class InitialRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = ['Nombre', 'Apellidos', 'NumeroIdentificacion', 'CorreoElectronico']
    
    def create(self, validated_data):
        numero_identificacion = validated_data['NumeroIdentificacion']
        correo_electronico = validated_data['CorreoElectronico']
        
        # Verificar si ya existe un usuario con el mismo document_number
        if User.objects.filter(document_number=numero_identificacion).exists():
            raise ValidationError(f"El número de identificación {numero_identificacion} ya está en uso.")
        
        user = User.objects.create_user(
            document_number=numero_identificacion,
            email=correo_electronico,
            password=numero_identificacion
        )
        # Crear el grupo de estudiantes si no existe
        estudiantes_group, created = Group.objects.get_or_create(name='Estudiantes')
        user.groups.add(estudiantes_group)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        
        # Crear el registro del estudiante
        estudiante = Estudiante.objects.create(
            user=user,
            Nombre=validated_data['Nombre'],
            Apellidos=validated_data['Apellidos'],
            NumeroIdentificacion=numero_identificacion,
            CorreoElectronico=correo_electronico
        )
        return estudiante

class ProgressiveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = [
            'Foto', 'CiudadNacimiento', 'ConfirmacionCorreo', 'NumeroCelular',
            'Genero', 'FechaNacimiento', 'DepartamentoResidencia', 'CiudadResidencia', 'DireccionResidencia',
            'EntidadSalud', 'NombreColegio', 'EstamentoColegio', 'GradoEscolaridad', 'ModuloMatricular',
            'NombreAcudiente', 'NumeroCelularAcudiente', 'TieneDiscapacidad', 'TipoDiscapacidad',
            'DescripcionDiscapacidad', 'TipoVinculacion', 'ValorConsignado', 'NumeroRecibo', 'FechaConsignacion',
            'NombreResponsablePago', 'TipoIdentificacionResponsablePago', 'NumeroIdentificacionResponsablePago',
            'DireccionResidenciaResponsablePago', 'NumeroCelularResponsablePago', 'CorreoElectronicoResponsablePago',
            'DocumentoIdentidad', 'ReciboPago', 'ConstanciaEstudio'
        ]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        # Actualizamos el email del usuario si se envía en la actualización
        if 'CorreoElectronico' in validated_data:
            instance.user.email = validated_data['CorreoElectronico']
            instance.user.save()
        instance.is_profile_complete = True
        instance.save()
        return instance


class EstudianteSerializer(serializers.ModelSerializer):
    modulo = serializers.PrimaryKeyRelatedField(queryset=Modulo.objects.all())
    class Meta:
        model = Estudiante
        fields = '__all__'
    
    def validate(self, data):
        if data['CorreoElectronico'] != data['ConfirmacionCorreo']:
            raise serializers.ValidationError({"CorreoElectronico": "Los correos electrónicos no coinciden"})
        if data['TieneDiscapacidad'] and not data.get('TipoDiscapacidad'):
            raise serializers.ValidationError({"TipoDiscapacidad": "Este campo es obligatorio si el estudiante tiene una discapacidad."})
        if data['EstamentoColegio'] == 'Publico' and not data.get('ConstanciaEstudio'):
            raise serializers.ValidationError({"ConstanciaEstudio": "Este campo es obligatorio para estudiantes de colegios públicos."})
        return data
