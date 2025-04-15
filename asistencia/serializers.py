from rest_framework import serializers
from .models import Asistencia

class AsistenciaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Asistencia.
    """
    class Meta:
        model = Asistencia
        fields = '__all__'
        read_only_fields = [
            'id_asistencia'
        ]