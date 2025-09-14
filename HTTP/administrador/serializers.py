from rest_framework import serializers
from .models import Administrador

class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = '__all__' 
        
        # No incluir password en los campos editables directamente
        extra_kwargs = {
            'contrasena': {'write_only': True},
        }
