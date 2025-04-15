from rest_framework import serializers
from .models import Estudiante

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = '__all__' 
        
        # No incluir password en los campos editables directamente
        extra_kwargs = {
            'password': {'write_only': True},
        }


