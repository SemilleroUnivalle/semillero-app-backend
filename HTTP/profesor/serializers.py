from rest_framework import serializers
from .models import Profesor
from modulo.models import Modulo
from modulo.serializers import ModuloProfesorSerializer
from auditlog.models import LogEntry
from .auditlog_serializer import LogEntrySerializerProfesor

class ProfesorSerializer(serializers.ModelSerializer):
    audit_hoja_vida = LogEntrySerializerProfesor(read_only=True)
    audit_certificado_laboral = LogEntrySerializerProfesor(read_only=True)
    audit_certificado_academico = LogEntrySerializerProfesor(read_only=True)
    audit_documento_identidad = LogEntrySerializerProfesor(read_only=True)
    audit_rut = LogEntrySerializerProfesor(read_only=True)
    audit_certificado_bancario = LogEntrySerializerProfesor(read_only=True)

    class Meta:
        model = Profesor
        fields = '__all__' 

class ProfesorModuloSerializer(serializers.ModelSerializer):
    modulo = ModuloProfesorSerializer(read_only=True)
    audit_hoja_vida = LogEntrySerializerProfesor(read_only=True)
    audit_certificado_laboral = LogEntrySerializerProfesor(read_only=True)
    audit_certificado_academico = LogEntrySerializerProfesor(read_only=True)
    audit_documento_identidad = LogEntrySerializerProfesor(read_only=True)
    audit_rut = LogEntrySerializerProfesor(read_only=True)
    audit_certificado_bancario = LogEntrySerializerProfesor(read_only=True)

    class Meta:
        model = Profesor
        fields = '__all__' 

class AsignacionProfesorSerializer(serializers.Serializer):
    id_profesor = serializers.IntegerField()
    id_modulo = serializers.IntegerField()

    def validate(self, data):
        try:
            profesor = Profesor.objects.get(id_profesor=data['id_profesor'])
        except Profesor.DoesNotExist:
            raise serializers.ValidationError("Profesor no encontrado")

        try:
            modulo = Modulo.objects.get(id_modulo=data['id_modulo'])
        except Modulo.DoesNotExist:
            raise serializers.ValidationError("Módulo no encontrado")

        return data

class LogEntrySerializer(serializers.ModelSerializer):
    usuario = serializers.SerializerMethodField()

    class Meta:
        model = LogEntry
        fields = '__all__'

    def get_usuario(self, obj):
        return obj.actor.username if obj.actor else None