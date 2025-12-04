from rest_framework import serializers
from auditlog.models import LogEntry

class LogEntrySerializerEstudiante(serializers.ModelSerializer):
    usuario = serializers.SerializerMethodField()
    class Meta:
        model = LogEntry
        fields = ['timestamp', 'id', 'usuario']
        ref_name = "LogEntryEstudianteInscripcion"

    def get_usuario(self, obj):
        return obj.actor.first_name +" "+ obj.actor.last_name if obj.actor else None