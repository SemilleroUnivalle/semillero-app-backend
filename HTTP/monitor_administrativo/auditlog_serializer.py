from rest_framework import serializers
from auditlog.models import LogEntry

class LogEntrySerializerMonitorAdministrativo(serializers.ModelSerializer):
    usuario = serializers.SerializerMethodField()
    class Meta:
        model = LogEntry
        fields = '__all__'

    def get_usuario(self, obj):
        return obj.actor.first_name +" "+ obj.actor.last_name if obj.actor else None