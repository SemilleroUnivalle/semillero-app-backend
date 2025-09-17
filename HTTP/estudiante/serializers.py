from rest_framework import serializers
from .models import Estudiante
from acudiente.serializers import AcudienteSerializer

class EstudianteSerializer(serializers.ModelSerializer):
    acudiente = AcudienteSerializer(read_only=True)

    class Meta:
        model = Estudiante
        fields = '__all__'
        
class LoteEliminarSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        help_text="Lista de IDs de estudiantes a eliminar"
    )
       

