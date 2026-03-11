from rest_framework import serializers
from .models import Asistencia

from inscripcion.models import Inscripcion
from inscripcion.serializers import InscripcionEstudianteSoloSerializer

from modulo.serializers import ModuloReadSerializer
from modulo.models import Modulo

class AsistenciaSerializer(serializers.ModelSerializer):
    
    id_inscripcion = InscripcionEstudianteSoloSerializer(read_only=True)

    id_inscripcion_id = serializers.PrimaryKeyRelatedField(
        queryset=Inscripcion.objects.all(), 
        source='id_inscripcion',           
        write_only=True                    
    )

    class Meta:
        model = Asistencia
        fields = '__all__'
        read_only_fields = [
            'id_asistencia'
        ]