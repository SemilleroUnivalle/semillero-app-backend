from rest_framework import serializers
from .models import SeguimientoAcademico

class SeguimientoAcademicoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo SeguimientoAcademico.
    
    Permite la validación y serialización de los datos del seguimiento académico.
    """
    class Meta:
        model = SeguimientoAcademico
        fields = '__all__'
        read_only_fields = ('id_seguimiento_academico',)