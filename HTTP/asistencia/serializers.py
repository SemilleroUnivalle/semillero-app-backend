from rest_framework import serializers
from .models import Asistencia
from inscripcion.serializers import InscripcionEstudianteSoloSerializer

class AsistenciaSerializer(serializers.ModelSerializer):
    
    id_inscripcion = InscripcionEstudianteSoloSerializer(read_only=True)

    class Meta:
        model = Asistencia
        fields = '__all__'
        read_only_fields = [
            'id_asistencia'
        ]