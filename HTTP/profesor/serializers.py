from rest_framework import serializers
from .models import Profesor
from modulo.models import Modulo

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = '__all__' 
        
        # No incluir contraseña en los campos editables directamente
        extra_kwargs = {
            'contrasena': {'write_only': True},
        }

class AsignacionProfesorSerializer(serializers.Serializer):
    id_profesor = serializers.IntegerField()
    id_modulo = serializers.IntegerField()

    def validate(self, data):
        try:
            profesor = Profesor.objects.get(id_profesor=data['id_profesor'])
        except Profesor.DoesNotExist:
            raise serializers.ValidationError("Profesor no encontrado")

        try:
            modulo = Modulo.objects.get(id_modulo=data['id_modulo'])
        except Modulo.DoesNotExist:
            raise serializers.ValidationError("Módulo no encontrado")

        return data