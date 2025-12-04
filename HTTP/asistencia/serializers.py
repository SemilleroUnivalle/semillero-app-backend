from rest_framework import serializers
from .models import Asistencia

from inscripcion.models import Inscripcion
from inscripcion.serializers import InscripcionEstudianteSoloSerializer

from modulo.serializers import ModuloReadSerializer
from modulo.models import Modulo

class AsistenciaSerializer(serializers.ModelSerializer):
    
    id_inscripcion = InscripcionEstudianteSoloSerializer(read_only=True)

    id_inscripcion_id = serializers.PrimaryKeyRelatedField(
        queryset=Inscripcion.objects.all(), # Importante: Define qué IDs son válidos
        source='id_inscripcion',           # Mapea este campo de nuevo al campo del modelo
        write_only=True                    # Hace que solo se use para escribir, no para mostrar
    )

    class Meta:
        model = Asistencia
        fields = '__all__'
        read_only_fields = [
            'id_asistencia'
        ]