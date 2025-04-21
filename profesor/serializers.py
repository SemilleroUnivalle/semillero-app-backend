from rest_framework import serializers
from .models import Profesor

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = '__all__' 
        
        # No incluir contraseña en los campos editables directamente
        extra_kwargs = {
            'contrasena': {'write_only': True},
        }
