from rest_framework import serializers
from .models import Estudiante
from acudiente.serializers import AcudienteSerializer
from auditlog.models import LogEntry
from .auditlog_serializer import LogEntrySerializerEstudiante

class EstudianteSerializer(serializers.ModelSerializer):
    acudiente = AcudienteSerializer(read_only=True)
    audit_foto = LogEntrySerializerEstudiante(read_only=True)
    audit_documento_identidad = LogEntrySerializerEstudiante(read_only=True)
    audit_informacion = LogEntrySerializerEstudiante(read_only=True)

    class Meta:
        model = Estudiante
        fields = '__all__'

class EstudianteSerializerMatricula(serializers.ModelSerializer):
    acudiente = AcudienteSerializer(read_only=True)
    audit_foto = LogEntrySerializerEstudiante(read_only=True)
    audit_documento_identidad = LogEntrySerializerEstudiante(read_only=True)
    audit_informacion = LogEntrySerializerEstudiante(read_only=True)

    class Meta:
        model = Estudiante
        fields = '__all__'

class EstudianteLista(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = ['id_estudiante', 'nombre', 'apellido', 'numero_documento', 'email', 'colegio']

class LogEntrySerializer(serializers.ModelSerializer):
    usuario = serializers.SerializerMethodField()

    class Meta:
        model = LogEntry
        fields = '__all__'

    def get_usuario(self, obj):
        return obj.actor.username if obj.actor else None
       

