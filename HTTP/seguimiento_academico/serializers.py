from rest_framework import serializers
from .models import SeguimientoAcademico

class SeguimientoAcademicoSerializer(serializers.ModelSerializer):
    nota_final = serializers.ReadOnlyField()
    estudiante_nombre = serializers.CharField(source='id_inscripcion.id_estudiante.nombre', read_only=True)
    estudiante_apellido = serializers.CharField(source='id_inscripcion.id_estudiante.apellido', read_only=True)
    grupo_nombre = serializers.CharField(source='id_inscripcion.grupo.nombre', read_only=True)

    class Meta:
        model = SeguimientoAcademico
        fields = [
            'id_seguimiento', 'id_inscripcion', 'estudiante_nombre', 'estudiante_apellido', 
            'grupo_nombre', 'seguimiento_1', 'seguimiento_2', 
            'nota_conceptual_docente', 'nota_conceptual_estudiante', 
            'nota_final', 'fecha_ultimo_cambio', 'observaciones'
        ]
        read_only_fields = ('id_seguimiento', 'fecha_ultimo_cambio')